/* ==========================================================
   EchoDesk Layout
========================================================== */

document.addEventListener("DOMContentLoaded", () => {

    const appShell = document.querySelector(".app-shell");
    const sidebar = document.querySelector(".sidebar");
    const overlay = document.querySelector(".sidebar-overlay");

    const menuButton = document.getElementById("menuToggle");

    const themeButton = document.getElementById("themeToggle");



    /* ===========================================
       Sidebar
    =========================================== */

    if(menuButton){

        menuButton.addEventListener("click",()=>{

            appShell.classList.toggle("is-sidebar-open");

        });

    }



    if(overlay){

        overlay.addEventListener("click",()=>{

            appShell.classList.remove("is-sidebar-open");

        });

    }



    /* ===========================================
       Dark Mode
    =========================================== */

    const savedTheme = localStorage.getItem("theme");

    if(savedTheme){

        document.documentElement.setAttribute(
            "data-theme",
            savedTheme
        );

    }

    if(themeButton){

        themeButton.addEventListener("click",()=>{

            const current =
                document.documentElement.getAttribute("data-theme");

            const next =
                current === "dark"
                    ? "light"
                    : "dark";

            document.documentElement.setAttribute(
                "data-theme",
                next
            );

            localStorage.setItem(
                "theme",
                next
            );

            themeButton.textContent =
                next === "dark"
                    ? "☀️"
                    : "🌙";

        });

    }



    /* ===========================================
       Active Sidebar Link
    =========================================== */

    const currentPath =
        window.location.pathname;

    document
        .querySelectorAll(".sidebar__link")
        .forEach(link=>{

            if(link.getAttribute("href")===currentPath){

                link.classList.add("is-active");

            }

        });



});