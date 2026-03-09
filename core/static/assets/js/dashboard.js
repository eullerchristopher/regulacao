function mostrarPagina(paginaId) {
    // Esconde todas as páginas
    const paginas = document.querySelectorAll('.pagina');
    paginas.forEach(p => p.classList.remove('ativa'));

    // Mostra a página selecionada
    const paginaSelecionada = document.getElementById(paginaId);
    if (paginaSelecionada) {
        paginaSelecionada.classList.add('ativa');
    }

    // Atualiza o menu ativo
    const itensMenu = document.querySelectorAll('.sidebar ul li');
    itensMenu.forEach(item => item.classList.remove('active'));
    const itemAtivo = Array.from(itensMenu).find(li => li.getAttribute('onclick')?.includes(paginaId));
    if (itemAtivo) itemAtivo.classList.add('active');
}

 // Script do acordeão
        document.querySelectorAll('.acordeao-header').forEach(header => {
            header.addEventListener('click', () => {
                const body = header.nextElementSibling;
                body.style.display = body.style.display === 'block' ? 'none' : 'block';
                header.querySelector('span:last-child').textContent = body.style.display === 'block' ? '▲' : '▼';
            });
        });