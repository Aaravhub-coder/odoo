document.addEventListener("DOMContentLoaded", () => {
  // ================= UI CORE SELECTORS =================
  const loginBtn = document.getElementById("loginBtn");
  const loginScreen = document.getElementById("login-screen");
  const appScreen = document.getElementById("app");
  const navItems = document.querySelectorAll(".nav-item");
  const views = document.querySelectorAll("section.view");

  // ================= LOGIN VIEW TRANSITION =================
  if (loginBtn && loginScreen && appScreen) {
    loginBtn.addEventListener("click", (e) => {
      e.preventDefault();

      // 1. Fade out the login dashboard panel gracefully via CSS transition
      loginScreen.classList.add("hidden");
      
      // 2. Clear from layout display and flip application viewport to grid structure
      setTimeout(() => {
        loginScreen.style.display = "none";
        appScreen.classList.add("visible");
        
        // 3. Render analytical components once container elements exist in viewport
        initDashboardCharts();
      }, 600); // Matches your exact .hidden CSS 0.6s ease duration
    });
  }

  // ================= SIDEBAR INTERNAL NAVIGATION =================
  navItems.forEach(item => {
    item.addEventListener("click", () => {
      const targetView = item.getAttribute("data-view");
      if (!targetView) return;

      // Toggle navigational active visual states
      navItems.forEach(nav => nav.classList.remove("active"));
      item.classList.add("active");

      // Toggle core viewport section displays
      views.forEach(view => {
        if (view.id === `view-${targetView}`) {
          view.classList.add("active");
        } else {
          view.classList.remove("active");
        }
      });
    });
  });

  // ================= TRANSITOPS ANALYTICS ENGINE (CHART.JS) =================
  function initDashboardCharts() {
    // Shared styling configuration variables to seamlessly match your CSS theme variables
    const textMutedColor = '#8695B7';
    const borderGridColor = '#263252';

    // 1. Fleet Utilization Trend Chart (Line)
    const utilCtx = document.getElementById("utilChart");
    if (utilCtx) {
      new Chart(utilCtx.getContext("2d"), {
        type: 'line',
        data: {
          labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
          datasets: [{
            label: 'Utilization %',
            data: [88, 91, 89, 93, 95, 92, 94.2],
            borderColor: '#14E0B4',         // var(--teal)
            backgroundColor: 'rgba(20, 224, 180, 0.05)', // Subtle teal tint
            borderWidth: 2,
            tension: 0.3,
            fill: true
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { display: false } },
          scales: {
            y: { 
              grid: { color: borderGridColor }, 
              ticks: { color: textMutedColor }, 
              min: 80, 
              max: 100 
            },
            x: { 
              grid: { display: false }, 
              ticks: { color: textMutedColor } 
            }
          }
        }
      });
    }

    // 2. Operational Cost Split Chart (Doughnut)
    const costCtx = document.getElementById("costChart");
    if (costCtx) {
      new Chart(costCtx.getContext("2d"), {
        type: 'doughnut',
        data: {
          labels: ['Fuel', 'Maintenance', 'Tolls & Other'],
          datasets: [{
            data: [18420, 9860, 2140],
            backgroundColor: [
              '#14E0B4', // var(--teal)
              '#4C8DFF', // var(--blue)
              '#FFB238'  // var(--amber)
            ],
            borderWidth: 0,
            weight: 0.5
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { display: false } },
          cutout: '75%'
        }
      });
    }
  }
});