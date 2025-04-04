import React, { useEffect } from 'react';

const SidebarToggle = () => {
  useEffect(() => {
    // Remove the Healthcare Assistant header
    const header = document.querySelector('.chat-header');
    if (header) {
      header.style.display = 'none';
    }
    
    // Create sidebar toggle button
    const mainContent = document.querySelector('.chat-container');
    const sidebar = document.querySelector('.sidebar');
    
    // Create toggle button
    const toggleButton = document.createElement('button');
    toggleButton.innerHTML = '&#9776;'; // Hamburger menu icon
    toggleButton.className = 'sidebar-toggle';
    toggleButton.setAttribute('aria-label', 'Toggle Sidebar');
    
    // Insert toggle button
    document.body.appendChild(toggleButton);
    
    // Add toggle functionality
    toggleButton.addEventListener('click', function() {
      if (sidebar) {
        sidebar.classList.toggle('collapsed');
        mainContent.classList.toggle('expanded');
      }
    });

    // Cleanup function
    return () => {
      if (toggleButton && toggleButton.parentNode) {
        toggleButton.parentNode.removeChild(toggleButton);
      }
    };
  }, []);
  
  return null;
};

export default SidebarToggle; 