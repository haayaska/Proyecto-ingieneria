const menu1 = document.querySelector(".menu");
const menu = document.querySelector(".menu-navegacion");


console.log(menu)
console.log(menu1)


menu1.addEventListener("click",()=>{
 menu.classList.toggle("spread")

})

window.addEventListener("click", e=>{
    if(menu.classList.contains("spread")
        && e.target !=menu && e.target != menu1    ){
        
        
            menu.classList.toggle("spread")

    }
})