(() => {
  // Sticky top
  const top = document.querySelector(".rq-top");
  if (top) {
    const onScroll = () => top.classList.toggle("scrolled", window.scrollY > 12);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  // Reveal
  const io = new IntersectionObserver(
    (entries) => entries.forEach((e) => e.isIntersecting && e.target.classList.add("in")),
    { threshold: 0.12, rootMargin: "0px 0px -8% 0px" }
  );
  document.querySelectorAll(".reveal").forEach((el) => io.observe(el));

  // Facets / sizes
  document.querySelectorAll(".facets button, .sizes button").forEach((btn) => {
    btn.addEventListener("click", () => {
      btn.parentElement.querySelectorAll("button").forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
    });
  });

  // Video mute / play toggle
  document.querySelectorAll("[data-rq-video]").forEach((wrap) => {
    const video = wrap.querySelector("video");
    const muteBtn = wrap.querySelector("[data-mute]");
    const playBtn = wrap.querySelector("[data-play]");
    if (!video) return;
    video.muted = true;
    video.play().catch(() => {});
    muteBtn?.addEventListener("click", () => {
      video.muted = !video.muted;
      muteBtn.textContent = video.muted ? "Sound" : "Mute";
    });
    playBtn?.addEventListener("click", () => {
      if (video.paused) {
        video.play();
        playBtn.textContent = "Pause";
      } else {
        video.pause();
        playBtn.textContent = "Play";
      }
    });
  });

  // Home product showcase slider
  document.querySelectorAll("[data-showcase]").forEach((root) => {
    const track = root.querySelector(".track");
    const slides = [...root.querySelectorAll(".slide")];
    const dotsWrap = root.querySelector(".dots");
    if (!track || !slides.length) return;
    let i = 0;
    let timer;

    slides.forEach((_, idx) => {
      const d = document.createElement("button");
      d.type = "button";
      d.setAttribute("aria-label", `Go to look ${idx + 1}`);
      if (idx === 0) d.classList.add("on");
      d.addEventListener("click", () => go(idx));
      dotsWrap?.appendChild(d);
    });

    const sync = () => {
      track.style.transform = `translateX(-${i * 100}%)`;
      dotsWrap?.querySelectorAll("button").forEach((d, di) => d.classList.toggle("on", di === i));
    };
    const go = (n) => {
      i = (n + slides.length) % slides.length;
      sync();
      restart();
    };
    const restart = () => {
      clearInterval(timer);
      timer = setInterval(() => go(i + 1), 5200);
    };

    root.querySelectorAll("[data-next]").forEach((b) => b.addEventListener("click", () => go(i + 1)));
    root.querySelectorAll("[data-prev]").forEach((b) => b.addEventListener("click", () => go(i - 1)));

    let startX = 0;
    track.addEventListener("touchstart", (e) => { startX = e.touches[0].clientX; }, { passive: true });
    track.addEventListener("touchend", (e) => {
      const dx = e.changedTouches[0].clientX - startX;
      if (Math.abs(dx) > 40) go(dx < 0 ? i + 1 : i - 1);
    });

    sync();
    restart();
  });

  // PDP gallery slider
  document.querySelectorAll("[data-gal-slider]").forEach((root) => {
    const slidesEl = root.querySelector(".slides");
    const frames = [...root.querySelectorAll(".slides .frame")];
    const thumbs = [...root.querySelectorAll(".thumbs button")];
    const progress = root.querySelector(".progress span");
    if (!slidesEl || !frames.length) return;
    let i = 0;
    const sync = () => {
      slidesEl.style.transform = `translateX(-${i * 100}%)`;
      thumbs.forEach((t, ti) => t.classList.toggle("on", ti === i));
      if (progress) progress.style.width = `${((i + 1) / frames.length) * 100}%`;
    };
    const go = (n) => {
      i = (n + frames.length) % frames.length;
      sync();
    };
    root.querySelector("[data-prev]")?.addEventListener("click", () => go(i - 1));
    root.querySelector("[data-next]")?.addEventListener("click", () => go(i + 1));
    thumbs.forEach((t, ti) => t.addEventListener("click", () => go(ti)));
    sync();
  });

  // Sticky ATC
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
