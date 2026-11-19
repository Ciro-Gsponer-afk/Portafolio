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

// DRAG & DROP: al soltar, se manda la nueva lista de ids al servidor.
document.querySelectorAll("[data-ordenar]").forEach((contenedor) => {
  let elementoArrastrado = null;

  contenedor.querySelectorAll('[draggable="true"]').forEach((elemento) => {
    elemento.addEventListener("dragstart", (evento) => {
      elementoArrastrado = elemento;
      elemento.classList.add("arrastrando");
      evento.dataTransfer.effectAllowed = "move";
      evento.dataTransfer.setData("text/plain", elemento.dataset.id || "");
    });

    elemento.addEventListener("dragend", () => {
      elementoArrastrado = null;
      elemento.classList.remove("arrastrando");
    });
  });

  contenedor.addEventListener("dragover", (evento) => {
    evento.preventDefault(); // Sin esto el navegador no permite soltar.
    if (!elementoArrastrado) return;

    const destino = evento.target.closest('[draggable="true"]');
    if (!destino || destino === elementoArrastrado || destino.parentElement !== contenedor) {
      return;
    }

    const caja = destino.getBoundingClientRect();
    const esCuadricula = getComputedStyle(contenedor).display === "grid";
    // En grillas (proyectos) se compara por X; en listas, por Y.
    const despues = esCuadricula
      ? evento.clientX > caja.left + caja.width / 2
      : evento.clientY > caja.top + caja.height / 2;

    contenedor.insertBefore(elementoArrastrado, despues ? destino.nextSibling : destino);
  });

  contenedor.addEventListener("drop", async (evento) => {
    evento.preventDefault();
    if (!elementoArrastrado) return;

    const ids = Array.from(
      contenedor.querySelectorAll('[draggable="true"]'),
      (elemento) => Number(elemento.dataset.id)
    );
    const token = document.querySelector('meta[name="csrf-token"]')?.content || "";

    try {
      const respuesta = await fetch(`/editar/${contenedor.dataset.ordenar}/reordenar`, {
        method: "POST",
        headers: {"Content-Type": "application/json", "X-CSRFToken": token},
        body: JSON.stringify({ids}),
      });
      if (!respuesta.ok) throw new Error("No se pudo guardar el nuevo orden");
    } catch (error) {
      console.error(error);
    }
  });
});
