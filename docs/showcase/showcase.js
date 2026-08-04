(() => {
  const top = document.querySelector(".sx-top");
  if (top) {
    const onScroll = () => top.classList.toggle("scrolled", window.scrollY > 12);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  const io = new IntersectionObserver(
    (entries) => entries.forEach((e) => e.isIntersecting && e.target.classList.add("in")),
    { threshold: 0.12, rootMargin: "0px 0px -8% 0px" }
  );
  document.querySelectorAll(".reveal").forEach((el) => io.observe(el));

  document.querySelectorAll(".facets button").forEach((btn) => {
    btn.addEventListener("click", () => {
      btn.parentElement.querySelectorAll("button").forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
    });
  });

  document.querySelectorAll(".sizes button").forEach((btn) => {
    btn.addEventListener("click", () => {
      btn.parentElement.querySelectorAll("button").forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
    });
  });

  document.querySelectorAll(".gal-swatch").forEach((gal) => {
    const main = gal.querySelector(".main img");
    gal.querySelectorAll(".thumbs button").forEach((btn) => {
      btn.addEventListener("click", () => {
        gal.querySelectorAll(".thumbs button").forEach((b) => b.classList.remove("active"));
        btn.classList.add("active");
        const img = btn.querySelector("img");
        if (main && img) main.src = img.src;
      });
    });
  });

  document.querySelectorAll(".gal-reel").forEach((reel) => {
    const slides = reel.querySelector(".slides");
    const frames = reel.querySelectorAll(".slides .frame");
    const dots = reel.querySelector(".dots");
    if (!slides || !frames.length || !dots) return;
    let i = 0;
    frames.forEach((_, idx) => {
      const b = document.createElement("button");
      if (idx === 0) b.classList.add("on");
      b.addEventListener("click", () => {
        i = idx;
        slides.style.transform = `translateX(-${i * 100}%)`;
        dots.querySelectorAll("button").forEach((d, di) => d.classList.toggle("on", di === i));
      });
      dots.appendChild(b);
    });
    setInterval(() => {
      i = (i + 1) % frames.length;
      slides.style.transform = `translateX(-${i * 100}%)`;
      dots.querySelectorAll("button").forEach((d, di) => d.classList.toggle("on", di === i));
    }, 4200);
  });

  const sticky = document.querySelector(".sticky-atc");
  const atc = document.querySelector("[data-atc]");
  if (sticky && atc) {
    const sio = new IntersectionObserver(
      ([e]) => sticky.classList.toggle("show", !e.isIntersecting),
      { threshold: 0 }
    );
    sio.observe(atc);
  }
})();
