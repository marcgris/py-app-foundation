(() => {
  const markerElement = document.getElementById("starter-ui-smoke-marker");
  if (!markerElement) {
    return;
  }

  markerElement.setAttribute("data-ready", "true");
})();
