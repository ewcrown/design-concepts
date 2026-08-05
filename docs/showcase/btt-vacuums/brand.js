(() => {
  const top = document.querySelector("[data-top]");
  if (top) {
    const on = () => top.classList.toggle("scrolled", scrollY > 8);
    on(); addEventListener("scroll", on, { passive: true });
  }
  const io = new IntersectionObserver(
    (es) => es.forEach((e) => e.isIntersecting && e.target.classList.add("in")),
    { threshold: 0.1 }
  );
  document.querySelectorAll(".reveal").forEach((el) => io.observe(el));
  document.querySelectorAll("[data-tabs] button, .sizes button").forEach((btn) => {
    btn.addEventListener("click", () => {
      btn.parentElement.querySelectorAll("button").forEach((b) => b.classList.remove("on","active"));
      btn.classList.add("on");
      btn.classList.add("active");
    });
  });
  document.querySelectorAll("[data-gal]").forEach((gal) => {
    const main = gal.querySelector("[data-main]");
    gal.querySelectorAll(".thumbs button").forEach((btn) => {
      btn.addEventListener("click", () => {
        gal.querySelectorAll(".thumbs button").forEach((b) => b.classList.remove("on"));
        btn.classList.add("on");
        const i = btn.querySelector("img");
        if (main && i) main.src = i.src.replace(/\/\d+\/\d+/, "/1200/1500");
      });
    });
  });
  const sticky = document.querySelector(".sticky-atc");
  const atc = document.querySelector("[data-atc]");
  if (sticky && atc) {
    new IntersectionObserver(([e]) => sticky.classList.toggle("show", !e.isIntersecting), { threshold: 0 }).observe(atc);
  }
})();
