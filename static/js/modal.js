
    function openCreateModal() {
    let modal = document.getElementById('postModal');
    if (!modal) {
        console.error("Modal not found!");
        return;
    }
    
    // Ensure modal is displayed
    modal.classList.remove('hidden');
    modal.style.display = 'flex';  // Ensures it is visible
}

function closeModal() {
    let modal = document.getElementById('postModal');
    if (!modal) {
        console.error("Modal not found!");
        return;
    }

    // Hide the modal properly
    modal.classList.add('hidden');
    modal.style.display = 'none';  // Ensures it is hidden
}



    
