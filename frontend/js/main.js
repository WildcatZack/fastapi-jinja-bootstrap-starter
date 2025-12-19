import 'bootstrap';

const tooltipTriggerList = Array.from(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
tooltipTriggerList.forEach((tooltipTriggerEl) => {
  return new window.bootstrap.Tooltip(tooltipTriggerEl);
});
