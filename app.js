// Add sidebar toggle functionality and remove header
document.addEventListener('DOMContentLoaded', function() {
  // Remove the Healthcare Assistant header
  const header = document.querySelector('header') || document.querySelector('.Healthcare.Assistant');
  if (header) {
    header.style.display = 'none';
  }
  
  // Create sidebar toggle button
  const mainContent = document.querySelector('main') || document.querySelector('.content-area');
  const sidebar = document.querySelector('aside') || document.querySelector('.sidebar');
  
  // Add console logs to help debug
  console.log('Header element:', header);
  console.log('Main content element:', mainContent);
  console.log('Sidebar element:', sidebar);
  
  // Create toggle button
  const toggleButton = document.createElement('button');
  toggleButton.innerHTML = '&#9776;'; // Hamburger menu icon
  toggleButton.className = 'sidebar-toggle';
  toggleButton.setAttribute('aria-label', 'Toggle Sidebar');
  
  // Insert toggle button at the top of main content
  if (mainContent) {
    mainContent.insertBefore(toggleButton, mainContent.firstChild);
  } else {
    document.body.appendChild(toggleButton);
  }
  
  // Add toggle functionality
  toggleButton.addEventListener('click', function() {
    if (sidebar) {
      sidebar.classList.toggle('collapsed');
      mainContent.classList.toggle('expanded');
    }
  });
}); 