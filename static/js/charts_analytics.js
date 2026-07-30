// Cyberpunk Chart.js Analytics Engine
document.addEventListener('DOMContentLoaded', () => {
  // Global Chart Defaults for Dark Cyberpunk Theme
  if (typeof Chart !== 'undefined') {
    Chart.defaults.color = '#B8C0D4';
    Chart.defaults.font.family = "'Rajdhani', 'Inter', sans-serif";
    Chart.defaults.font.size = 13;
    Chart.defaults.plugins.tooltip.backgroundColor = 'rgba(4, 6, 15, 0.9)';
    Chart.defaults.plugins.tooltip.borderColor = 'rgba(0, 245, 255, 0.4)';
    Chart.defaults.plugins.tooltip.borderWidth = 1;
    Chart.defaults.plugins.tooltip.titleColor = '#00F5FF';
    Chart.defaults.plugins.tooltip.bodyColor = '#FFFFFF';
    Chart.defaults.plugins.tooltip.padding = 12;
    Chart.defaults.plugins.tooltip.cornerRadius = 10;
  }

  // 1. Student Performance Line Graph
  const studentChartCtx = document.getElementById('studentPerformanceChart');
  if (studentChartCtx && typeof Chart !== 'undefined') {
    fetch('/analytics/chart-data/?type=performance')
      .then(res => res.json())
      .then(resData => {
        const ctx = studentChartCtx.getContext('2d');
        const gradient = ctx.createLinearGradient(0, 0, 0, 300);
        gradient.addColorStop(0, 'rgba(0, 245, 255, 0.35)');
        gradient.addColorStop(1, 'rgba(123, 63, 251, 0.02)');

        new Chart(studentChartCtx, {
          type: 'line',
          data: {
            labels: resData.labels,
            datasets: [{
              label: 'Exam Score (%)',
              data: resData.data,
              borderColor: '#00F5FF',
              borderWidth: 3,
              backgroundColor: gradient,
              fill: true,
              tension: 0.4,
              pointRadius: 6,
              pointBackgroundColor: '#00F5FF',
              pointBorderColor: '#04060F',
              pointHoverRadius: 9,
              pointHoverBackgroundColor: '#FFFFFF',
              pointHoverBorderColor: '#7B3FFB'
            }]
          },
          options: {
            responsive: true,
            scales: {
              x: { grid: { color: 'rgba(255, 255, 255, 0.05)' } },
              y: { min: 0, max: 100, grid: { color: 'rgba(255, 255, 255, 0.05)' } }
            }
          }
        });
      });
  }

  // 2. Admin Pass/Fail Doughnut Chart
  const passFailCtx = document.getElementById('adminPassFailChart');
  if (passFailCtx && typeof Chart !== 'undefined') {
    fetch('/analytics/chart-data/?type=pass_fail')
      .then(res => res.json())
      .then(resData => {
        new Chart(passFailCtx, {
          type: 'doughnut',
          data: {
            labels: resData.labels,
            datasets: [{
              data: resData.data,
              backgroundColor: ['#00FF9D', '#FF0055'],
              borderColor: '#04060F',
              borderWidth: 3,
              hoverOffset: 8
            }]
          },
          options: {
            responsive: true,
            plugins: {
              legend: { position: 'bottom', labels: { color: '#B8C0D4', padding: 16 } }
            }
          }
        });
      });
  }

  // 3. Admin Growth Bar Chart
  const growthCtx = document.getElementById('adminGrowthChart');
  if (growthCtx && typeof Chart !== 'undefined') {
    fetch('/analytics/chart-data/?type=admin_growth')
      .then(res => res.json())
      .then(resData => {
        new Chart(growthCtx, {
          type: 'bar',
          data: {
            labels: resData.labels,
            datasets: [
              { label: 'Students Enrolled', data: resData.students, backgroundColor: '#00F5FF', borderRadius: 8 },
              { label: 'Exams Conducted', data: resData.exams, backgroundColor: '#7B3FFB', borderRadius: 8 }
            ]
          },
          options: {
            responsive: true,
            scales: {
              x: { grid: { color: 'rgba(255, 255, 255, 0.05)' } },
              y: { grid: { color: 'rgba(255, 255, 255, 0.05)' } }
            },
            plugins: {
              legend: { position: 'top', labels: { color: '#B8C0D4' } }
            }
          }
        });
      });
  }

  // 4. Department Student Distribution Chart
  const deptCtx = document.getElementById('adminDepartmentChart');
  if (deptCtx && typeof Chart !== 'undefined') {
    fetch('/analytics/chart-data/?type=department_distribution')
      .then(res => res.json())
      .then(resData => {
        new Chart(deptCtx, {
          type: 'bar',
          data: {
            labels: resData.labels,
            datasets: [{
              label: 'Students Enrolled',
              data: resData.data,
              backgroundColor: ['#00F5FF', '#3EA6FF', '#7B3FFB', '#00FF9D', '#FFB800', '#FF0055'],
              borderRadius: 8
            }]
          },
          options: {
            responsive: true,
            scales: {
              x: { grid: { color: 'rgba(255, 255, 255, 0.05)' } },
              y: { grid: { color: 'rgba(255, 255, 255, 0.05)' } }
            },
            plugins: {
              legend: { display: false }
            }
          }
        });
      });
  }

  // 5. Exam Status Breakdown Chart
  const examStatusCtx = document.getElementById('adminExamStatusChart');
  if (examStatusCtx && typeof Chart !== 'undefined') {
    fetch('/analytics/chart-data/?type=exam_status_breakdown')
      .then(res => res.json())
      .then(resData => {
        new Chart(examStatusCtx, {
          type: 'pie',
          data: {
            labels: resData.labels,
            datasets: [{
              data: resData.data,
              backgroundColor: ['#00FF9D', '#00F5FF', '#7B3FFB', '#FFB800'],
              borderColor: '#04060F',
              borderWidth: 3
            }]
          },
          options: {
            responsive: true,
            plugins: {
              legend: { position: 'bottom', labels: { color: '#B8C0D4', padding: 16 } }
            }
          }
        });
      });
  }
});
