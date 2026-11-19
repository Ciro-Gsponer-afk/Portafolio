document.documentElement.classList.add("js");

const revelar = document.querySelectorAll(".reveal");

if ("IntersectionObserver" in window) {
  const observador = new IntersectionObserver(
    (entradas) => {
      entradas.forEach((entrada) => {
        if (entrada.isIntersecting) {
          entrada.target.classList.add("visible");
          observador.unobserve(entrada.target);
        }
      });
    },
    { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
  );

  revelar.forEach((elemento) => observador.observe(elemento));
} else {
  revelar.forEach((elemento) => elemento.classList.add("visible"));
}

const menuBoton = document.querySelector(".menu-toggle");
const menu = document.getElementById("navegacion");

if (menuBoton && menu) {
  const cerrarMenu = () => {
    menu.classList.remove("abierto");
    menuBoton.setAttribute("aria-expanded", "false");
  };

  menuBoton.addEventListener("click", () => {
    const abierto = menu.classList.toggle("abierto");
    menuBoton.setAttribute("aria-expanded", String(abierto));
  });

  menu.querySelectorAll("a").forEach((enlace) => {
    enlace.addEventListener("click", cerrarMenu);
  });

  window.addEventListener("resize", () => {
    if (window.innerWidth > 575) cerrarMenu();
  });
}

// MODALES: el mismo diálogo sirve para agregar y para editar.
document.querySelectorAll("[data-modal]").forEach((boton) => {
  boton.addEventListener("click", async () => {
    const modal = document.getElementById(boton.dataset.modal);
    if (!modal || typeof modal.showModal !== "function") return;

    const formulario = modal.querySelector("form");
    if (!formulario) return;

    // Arranca limpio para que no queden datos del elemento anterior.
    formulario.reset();
    const campoId = formulario.elements["item_id"];
    if (campoId) campoId.value = boton.dataset.id || "";

    // Si viene del lápiz, se piden los datos al servidor y se copian al form.
    if (boton.dataset.urlEditar) {
      try {
        const respuesta = await fetch(boton.dataset.urlEditar);
        if (respuesta.ok) {
          const datos = await respuesta.json();
          Object.entries(datos).forEach(([nombre, valor]) => {
            const campo = formulario.elements[nombre];
            if (campo) campo.value = valor ?? "";
          });
        }
      } catch (error) {
        console.error("No se pudieron cargar los datos del elemento.", error);
      }
    }

    modal.showModal();
  });
});

document.querySelectorAll("[data-cerrar-modal]").forEach((boton) => {
  boton.addEventListener("click", () => boton.closest("dialog")?.close());
});

document.querySelectorAll("dialog").forEach((modal) => {
  // Si el servidor devolvió errores, se abre solo el modal que falló.
  if (modal.querySelector(".error")) modal.showModal();

  modal.addEventListener("click", (evento) => {
    if (evento.target === modal) modal.close();
  });
});

// CONFIRMACIÓN: el botón sigue enviando el formulario solo si acepta.
document.querySelectorAll("[data-confirmar]").forEach((boton) => {
  boton.addEventListener("click", (evento) => {
    const mensaje = boton.dataset.confirmar || "¿Estás seguro?";
    if (!window.confirm(mensaje)) evento.preventDefault();
  });
});
