(function () {
  const top = document.querySelector(".site-top");
  if (top) {
    const onScroll = () => top.classList.toggle("is-scrolled", window.scrollY > 8);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  const reveals = document.querySelectorAll(".reveal");
  if (reveals.length && "IntersectionObserver" in window) {
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((e) => {
          if (e.isIntersecting) {
            e.target.classList.add("in");
            io.unobserve(e.target);
          }
        });
      },
      { threshold: 0.12, rootMargin: "0px 0px -8% 0px" }
    );
    reveals.forEach((el) => io.observe(el));
  } else {
    reveals.forEach((el) => el.classList.add("in"));
  }

  document.querySelectorAll(".gallery").forEach((gallery) => {
    const main = gallery.querySelector(".main img");
    const thumbs = gallery.querySelectorAll(".thumbs .img");
    thumbs.forEach((thumb) => {
      thumb.addEventListener("click", () => {
        const img = thumb.querySelector("img");
        if (!main || !img) return;
        main.src = img.src;
        thumbs.forEach((t) => t.classList.remove("is-active"));
        thumb.classList.add("is-active");
      });
    });
    if (thumbs[0]) thumbs[0].classList.add("is-active");
  });

  document.querySelectorAll(".sizes").forEach((group) => {
    group.querySelectorAll(".size").forEach((size) => {
      size.addEventListener("click", () => {
        group.querySelectorAll(".size").forEach((s) => s.classList.remove("active"));
        size.classList.add("active");
      });
    });
  });

  document.querySelectorAll(".filters").forEach((group) => {
    group.querySelectorAll(".chip").forEach((chip) => {
      chip.addEventListener("click", () => {
        group.querySelectorAll(".chip").forEach((c) => c.classList.remove("active"));
        chip.classList.add("active");
      });
    });
  });
})();
