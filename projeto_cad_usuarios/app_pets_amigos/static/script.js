// Exemplo de JavaScript para adicionar interatividade
document.addEventListener('DOMContentLoaded', function() {
    const links = document.querySelectorAll('nav ul li a');

    links.forEach(link => {
        link.addEventListener('click', function() {
            alert(`Você clicou em: ${this.innerText}`);
        });
    });
});
