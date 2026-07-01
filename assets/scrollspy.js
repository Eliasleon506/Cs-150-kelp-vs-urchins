// Highlights the active section in the sticky navbar as the page scrolls.
// Dash renders the layout client-side AFTER load, so the anchors/nav links do
// not exist on DOMContentLoaded — poll until they do, then attach once.
(function () {
  var ids = ["intro", "why-care", "why-suffering", "kelp-vs-urchins", "red-vs-purple", "how-to-help"];

  function attach() {
    var anchors = ids.map(function (id) { return document.getElementById(id); }).filter(Boolean);
    var links = document.querySelectorAll(".navbar .nav-link");
    if (anchors.length < ids.length || links.length === 0) return false;

    function setActive(id) {
      links.forEach(function (l) {
        var href = l.getAttribute("href") || "";
        l.classList.toggle("active-section", href === "#" + id);
      });
    }

    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) setActive(e.target.id);
      });
    }, { rootMargin: "-45% 0px -50% 0px", threshold: 0 });

    anchors.forEach(function (a) { observer.observe(a); });
    return true;
  }

  var tries = 0;
  var timer = setInterval(function () {
    tries += 1;
    if (attach() || tries > 100) clearInterval(timer);
  }, 200);
})();
