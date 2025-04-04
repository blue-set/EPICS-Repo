// Immediately invoked function to avoid global namespace pollution
(function() {
  // Function to apply our changes
  function applyChanges() {
    console.log("Applying sidebar toggle changes...");
    
    // Try to find elements with different possible selectors
    const header = document.querySelector('.chat-header') || 
                  document.querySelector('header') || 
                  document.querySelector('h1:contains("Healthcare")') ||
                  document.querySelector('.Healthcare.Assistant');
    
    const mainContent = document.querySelector('.chat-container') || 
                        document.querySelector('main') || 
                        document.querySelector('.content-area');
    
    const sidebar = document.querySelector('.sidebar') || 
                    document.querySelector('aside');
    
    console.log("Found elements:", { header, mainContent, sidebar });
    
    // Hide header if found
    if (header) {
      header.style.display = 'none';
      console.log("Header hidden");
    }
    
    // Create and append toggle button if not already present
    if (!document.querySelector('.sidebar-toggle')) {
      const toggleButton = document.createElement('button');
      toggleButton.innerHTML = '&#9776;';
      toggleButton.className = 'sidebar-toggle';
      toggleButton.setAttribute('aria-label', 'Toggle Sidebar');
      
      document.body.appendChild(toggleButton);
      console.log("Toggle button created");
      
      // Add toggle functionality
      toggleButton.addEventListener('click', function() {
        console.log("Toggle button clicked");
        if (sidebar) {
          sidebar.classList.toggle('collapsed');
          console.log("Sidebar class toggled:", sidebar.classList.contains('collapsed'));
        }
        if (mainContent) {
          mainContent.classList.toggle('expanded');
          console.log("Main content class toggled:", mainContent.classList.contains('expanded'));
        }
      });
    }
  }
  
  // Try multiple times to ensure React has rendered
  function attemptChanges() {
    applyChanges();
    
    // Keep trying every 500ms for 5 seconds total (10 attempts)
    for (let i = 1; i <= 10; i++) {
      setTimeout(applyChanges, i * 500);
    }
  }
  
  // Run on DOMContentLoaded
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', attemptChanges);
  } else {
    // DOM already loaded, run immediately
    attemptChanges();
  }
  
  // Also run on window load to be extra sure
  window.addEventListener('load', attemptChanges);
})(); 