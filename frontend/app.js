    const form = document.getElementById('schedule-form');
    const status = document.getElementById('status');

    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const onTime = document.getElementById('on-time').value;
      const offTime = document.getElementById('off-time').value;

      if (onTime && offTime) {
        status.textContent = `Lights scheduled: ON at ${onTime}, OFF at ${offTime}`;
        status.style.color = '#00ffea';
      } else {
        status.textContent = 'Please select both times.';
        status.style.color = '#ff007a';
      }

      setTimeout(() => {
        status.textContent = '';
      }, 3000);
    });
 