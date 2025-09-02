(function () {
  const API = (path) => `${window.API_BASE}${path}`;
  const tokenKey = "notes_access_token";
  const refreshKey = "notes_refresh_token";

  // ---- Auth helpers
  const getToken = () => localStorage.getItem(tokenKey);
  const setTokens = ({ access, refresh }) => {
    if (access) localStorage.setItem(tokenKey, access);
    if (refresh) localStorage.setItem(refreshKey, refresh);
    updateNav();
  };
  const clearTokens = () => {
    localStorage.removeItem(tokenKey);
    localStorage.removeItem(refreshKey);
    updateNav();
  };

  function authHeaders() {
    const t = getToken();
    return t ? { Authorization: `Bearer ${t}` } : {};
  }

  async function apiFetch(url, options = {}, tryRefresh = true) {
    const res = await fetch(url, {
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...(options.headers || {}),
        ...authHeaders(),
      },
    });

    // Try refresh on 401 once
    if (res.status === 401 && tryRefresh) {
      const refreshed = await refreshToken();
      if (refreshed) {
        return apiFetch(url, options, false);
      }
    }
    return res;
  }

  async function refreshToken() {
    const refresh = localStorage.getItem(refreshKey);
    if (!refresh) return false;
    try {
      const res = await fetch(API("/auth/refresh/"), {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ refresh }),
      });
      if (!res.ok) return false;
      const data = await res.json();
      if (data.access) {
        localStorage.setItem(tokenKey, data.access);
        return true;
      }
      return false;
    } catch {
      return false;
    }
  }

  // ---- Nav state
  function updateNav() {
    const navSignin = document.getElementById("nav-signin");
    const navSignout = document.getElementById("nav-signout");
    if (!navSignin || !navSignout) return;
    const hasToken = !!getToken();
    navSignin.style.display = hasToken ? "none" : "";
    navSignout.style.display = hasToken ? "" : "none";
  }

  function wireNavSignout() {
    const btn = document.getElementById("nav-signout");
    if (!btn) return;
    btn.addEventListener("click", () => {
      clearTokens();
      window.location.href = "/signin/";
    });
  }

  // ---- Page controllers
  async function onSigninPage() {
    const form = document.getElementById("signin-form");
    if (!form) return;

    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const email = form.email.value.trim();
      const password = form.password.value;
      const err = document.getElementById("signin-error");
      err.textContent = "";

      try {
        const res = await fetch(API("/auth/login/"), {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email: email, password }),
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || "Invalid credentials");
        setTokens({ access: data.access, refresh: data.refresh });
        window.location.href = "/notes/";
      } catch (e) {
        err.textContent = e.message || "Sign-in failed";
      }
    });
  }

  async function onSignupPage() {
    const form = document.getElementById("signup-form");
    if (!form) return;

    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const name = form.name.value.trim();
      const email = form.email.value.trim();
      const password = form.password.value;
      const err = document.getElementById("signup-error");
      err.textContent = "";

      try {
        const res = await fetch(API("/auth/signup/"), {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            user_name: name,
            user_email: email,
            password,
          }),
        });
        if (!res.ok) {
          const data = await res.json().catch(() => ({}));
          throw new Error(data.detail || "Sign-up failed");
        }

        // After signup, log in automatically
        const loginRes = await fetch(API("/auth/login/"), {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email, password }),
        });
        const loginData = await loginRes.json();
        if (!loginRes.ok) throw new Error(loginData.detail || "Auto login failed");

        setTokens({ access: loginData.access, refresh: loginData.refresh });
        window.location.href = "/notes/";
      } catch (e) {
        err.textContent = e.message || "Sign-up failed";
      }
    });
  }

  async function onNotesListPage() {
    const container = document.getElementById("notes-container");
    const empty = document.getElementById("notes-empty");
    const err = document.getElementById("notes-error");
    if (!container) return;

    err.textContent = "";
    container.innerHTML = "";
    try {
      const res = await apiFetch(API("/notes/"), { method: "GET" });
      if (!res.ok) throw new Error("Failed to load notes");
      const notes = await res.json();

      if (!notes || !notes.length) {
        empty.style.display = "";
        return;
      }
      empty.style.display = "none";

      for (const n of notes) {
        const card = document.createElement("div");
        card.className = "note-card";
        card.innerHTML = `
          <h3>${escapeHtml(n.note_title || "(Untitled)")}</h3>
          <p>${escapeHtml((n.note_content || "").slice(0, 140))}</p>
          <div class="card-actions">
            <a class="btn" href="/notes/${n.note_id}/">Edit</a>
            <button data-id="${n.note_id}" class="btn btn-danger btn-del">Delete</button>
          </div>
        `;
        container.appendChild(card);
      }

      // Wire deletes
      container.querySelectorAll(".btn-del").forEach((btn) => {
        btn.addEventListener("click", async () => {
          if (!confirm("Delete this note?")) return;
          const id = btn.getAttribute("data-id");
          const resp = await apiFetch(API(`/notes/${id}/`), { method: "DELETE" });
          if (!resp.ok && resp.status !== 204) {
            alert("Delete failed");
            return;
          }
          onNotesListPage(); // refresh
        });
      });
    } catch (e) {
      err.textContent = e.message || "Error loading notes";
    }
  }

  async function onNoteEditPage() {
    const form = document.getElementById("note-form");
    if (!form) return;
    const titleEl = document.getElementById("note-title");
    const contentEl = document.getElementById("note-content");
    const err = document.getElementById("note-error");
    const delBtn = document.getElementById("delete-note");
    const noteId = window.NOTE_ID || null;

    // Load existing note
    if (noteId) {
      try {
        const res = await apiFetch(API(`/notes/${noteId}/`), { method: "GET" });
        if (res.ok) {
          const data = await res.json();
          titleEl.value = data.note_title || "";
          contentEl.value = data.note_content || "";
        } else if (res.status === 404) {
          err.textContent = "Note not found.";
        } else {
          err.textContent = "Failed to load note.";
        }
      } catch {
        err.textContent = "Failed to load note.";
      }
    }

    // Save (create or update)
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      err.textContent = "";
      const payload = {
        note_title: titleEl.value.trim(),
        note_content: contentEl.value,
      };
      try {
        const res = await apiFetch(
          API(noteId ? `/notes/${noteId}/` : "/notes/"),
          {
            method: noteId ? "PUT" : "POST",
            body: JSON.stringify(payload),
          }
        );
        if (!res.ok) {
          const d = await res.json().catch(() => ({}));
          throw new Error(d.detail || "Save failed");
        }
        window.location.href = "/notes/";
      } catch (e) {
        err.textContent = e.message || "Save failed";
      }
    });

    if (delBtn && noteId) {
      delBtn.addEventListener("click", async () => {
        if (!confirm("Delete this note?")) return;
        const res = await apiFetch(API(`/notes/${noteId}/`), { method: "DELETE" });
        if (!res.ok && res.status !== 204) {
          err.textContent = "Delete failed";
          return;
        }
        window.location.href = "/notes/";
      });
    }
  }

  // ---- utils
  function escapeHtml(s) {
    return String(s)
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#039;");
  }

  // ---- init per page
  document.addEventListener("DOMContentLoaded", () => {
    updateNav();
    wireNavSignout();
    onSigninPage();
    onSignupPage();
    onNotesListPage();
    onNoteEditPage();
  });
})();
