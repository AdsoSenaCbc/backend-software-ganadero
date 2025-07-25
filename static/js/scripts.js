document.addEventListener('DOMContentLoaded', () => {
    const themeToggle = document.getElementById('theme-toggle');
    const themeIcon = document.getElementById('theme-icon');
    const body = document.body;

    // Cargar tema preferido desde localStorage o usar claro por defecto
    const savedTheme = localStorage.getItem('theme') || 'light';
    body.setAttribute('data-theme', savedTheme);
    if (savedTheme === 'dark') {
        themeIcon.classList.remove('fa-sun');
        themeIcon.classList.add('fa-moon');
        themeToggle.textContent = 'Modo Claro';
    }

    // Toggle de tema
    themeToggle.addEventListener('click', () => {
        const currentTheme = body.getAttribute('data-theme');
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';
        body.setAttribute('data-theme', newTheme);
        if(newTheme==='light'){
            themeIcon.classList.remove('fa-moon');
            themeIcon.classList.add('fa-sun');
        }else{
            themeIcon.classList.remove('fa-sun');
            themeIcon.classList.add('fa-moon');
        }
        localStorage.setItem('theme', newTheme);
    });

    // Validación básica de formularios
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', (e) => {
            const inputs = form.querySelectorAll('input[required]');
            let isValid = true;
            inputs.forEach(input => {
                if (!input.value.trim()) {
                    isValid = false;
                    input.style.borderColor = 'red';
                } else {
                    input.style.borderColor = '';
                }
            });
            if (!isValid) {
                e.preventDefault();
                alert('Por favor, completa todos los campos requeridos.');
            }
        });
    });
});

// ----- Sidebar y submenús -----
document.addEventListener('DOMContentLoaded', () => {
    const menuToggle  = document.getElementById('sidebarToggle');   // botón hamburguesa en navbar
    const sidebar     = document.getElementById('sidebar');
    const sidebarClose= document.getElementById('sidebarClose');

    if (menuToggle && sidebar) {
        menuToggle.addEventListener('click', () => sidebar.classList.toggle('active'));
    }
    if (sidebarClose) {
        sidebarClose.addEventListener('click', () => sidebar.classList.remove('active'));
    }

    // submenús (solo si algún enlace tiene data-bs-target)
    document.querySelectorAll('.nav-link.dropdown-toggle').forEach(toggle => {
        toggle.addEventListener('click', e => {
            e.preventDefault();
            const target = document.querySelector(toggle.dataset.bsTarget);
            if (target) target.classList.toggle('show');
        });
    });
});