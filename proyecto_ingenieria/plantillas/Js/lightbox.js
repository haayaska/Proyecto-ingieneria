const imagenes = document.querySelectorAll(".img-galeria")
const imageneslight = document.querySelector(".agregar-imagen")
const contenedorlight = document.querySelector(".imagen-light")

console.log(imagenes)
console.log(imageneslight)
console.log(contenedorlight)

imagenes.forEach(imagenes => {
    imagenes.addEventListener("click", ()=>{
        aparecerimagen(imagenes.getAttribute("src"))
    })

})

const aparecerimagen = ()=> {
    imageneslight.src = imagenes;
    contenedorlight.classList.toggle("show")
}