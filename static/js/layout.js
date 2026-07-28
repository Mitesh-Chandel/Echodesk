/* ==========================================================
   EchoDesk Layout
========================================================== */

document.addEventListener("DOMContentLoaded", () => {

    const appShell = document.querySelector(".app-shell");
    const overlay = document.querySelector(".sidebar-overlay");
    
    // Support multiple common trigger selectors
    const menuButton = 
        document.getElementById("menuToggle") || 
        document.querySelector(".topbar__toggle") || 
        document.querySelector("[data-menu-toggle]");

    const themeButton = document.getElementById("themeToggle");

    /* ===========================================
        Sidebar Toggle & Click-Outside
    =========================================== */
    if (menuButton && appShell) {
        menuButton.addEventListener("click", (e) => {
            e.preventDefault();
            appShell.classList.toggle("is-sidebar-open");
        });
    } else {
        console.warn("EchoDesk Layout: Menu toggle button not found in DOM. Ensure your button has id='menuToggle' in topbar.html.");
    }

    if (overlay && appShell) {
        overlay.addEventListener("click", () => {
            appShell.classList.remove("is-sidebar-open");
        });
    }

    // Close on Escape key press
    document.addEventListener("keydown", (e) => {
        if (e.key === "Escape" && appShell && appShell.classList.contains("is-sidebar-open")) {
            appShell.classList.remove("is-sidebar-open");
        }
    });

    /* ===========================================
        Dark Mode Toggle
    =========================================== */
    const savedTheme = localStorage.getItem("theme");

    if (savedTheme) {
        document.documentElement.setAttribute("data-theme", savedTheme);
    }

    if (themeButton) {
        themeButton.addEventListener("click", () => {
            const current = document.documentElement.getAttribute("data-theme");
            const next = current === "dark" ? "light" : "dark";

            document.documentElement.setAttribute("data-theme", next);
            localStorage.setItem("theme", next);
            themeButton.textContent = next === "dark" ? "☀️" : "🌙";
        });
    }

    /* ===========================================
        Active Navigation Link Highlight
    =========================================== */
    const currentPath = window.location.pathname;

    document.querySelectorAll(".sidebar__link").forEach(link => {
        if (link.getAttribute("href") === currentPath) {
            link.classList.add("is-active");
        }
    });

});