(() => {
  const top = document.querySelector("[data-top]");
  if (top) {
    const on = () => top.classList.toggle("scrolled", scrollY > 8);
    on(); addEventListener("scroll", on, { passive: true });
  }
  const io = new IntersectionObserver(
    (es) => es.forEach((e) => e.isIntersecting && e.target.classList.add("in")),
    { threshold: 0.12 }
  );
  document.querySelectorAll(".reveal").forEach((el) => io.observe(el));
  document.querySelectorAll("[data-tabs] button").forEach((btn) => {
    btn.addEventListener("click", () => {
      btn.parentElement.querySelectorAll("button").forEach((b) => b.classList.remove("on"));
      btn.classList.add("on");
    });
  });
  document.querySelectorAll("[data-gal]").forEach((gal) => {
    const main = gal.querySelector("[data-main]");
    gal.querySelectorAll("button").forEach((btn) => {
      btn.addEventListener("click", () => {
        gal.querySelectorAll("button").forEach((b) => b.classList.remove("on"));
        btn.classList.add("on");
        const i = btn.querySelector("img");
        if (main && i) main.src = i.src.replace(/\/\d+\/\d+/, "/1200/1500");
      });
    });
  });
})();
