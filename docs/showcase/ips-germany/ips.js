(() => {
  const top = document.querySelector(".top");
  if (top) {
    const onScroll = () => top.classList.toggle("scrolled", window.scrollY > 8);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }
  const io = new IntersectionObserver(
    (entries) => entries.forEach((e) => e.isIntersecting && e.target.classList.add("in")),
    { threshold: 0.12 }
  );
  document.querySelectorAll(".reveal").forEach((el) => io.observe(el));
  document.querySelectorAll(".facets button, .sizes button").forEach((btn) => {
    btn.addEventListener("click", () => {
      btn.parentElement.querySelectorAll("button").forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
    });
  });
  document.querySelectorAll("[data-gal]").forEach((gal) => {
    const main = gal.querySelector("[data-main]");
    gal.querySelectorAll(".thumbs button").forEach((btn) => {
      btn.addEventListener("click", () => {
        gal.querySelectorAll(".thumbs button").forEach((b) => b.classList.remove("on"));
        btn.classList.add("on");
        const img = btn.querySelector("img");
        if (main && img) main.src = img.src.replace("w=300", "w=1200");
      });
    });
  });
  const sticky = document.querySelector(".sticky-atc");
  const atc = document.querySelector("[data-atc]");
  if (sticky && atc) {
    new IntersectionObserver(([e]) => sticky.classList.toggle("show", !e.isIntersecting), { threshold: 0 }).observe(atc);
  }
})();
