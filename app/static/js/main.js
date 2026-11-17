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

document.querySelectorAll("[data-modal]").forEach((boton) => {
  boton.addEventListener("click", () => {
    const modal = document.getElementById(boton.dataset.modal);
    if (!modal || typeof modal.showModal !== "function") return;
    const formulario = modal.querySelector("form");
    if (formulario && boton.dataset.id) formulario.dataset.id = boton.dataset.id;
    modal.showModal();
  });
});

document.querySelectorAll("[data-cerrar-modal]").forEach((boton) => {
  boton.addEventListener("click", () => boton.closest("dialog")?.close());
});

document.querySelectorAll("dialog").forEach((modal) => {
  modal.addEventListener("click", (evento) => {
    if (evento.target === modal) modal.close();
  });
});

document.querySelectorAll("[data-confirmar]").forEach((boton) => {
  boton.addEventListener("click", () => {
    const mensaje = boton.dataset.confirmar || "¿Estás seguro?";
    if (window.confirm(mensaje)) boton.dispatchEvent(new CustomEvent("confirmado"));
  });
});
