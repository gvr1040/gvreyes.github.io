document.addEventListener("DOMContentLoaded", () => {
  // mobile nav toggle
  const toggle = document.querySelector(".nav-toggle");
  const links = document.querySelector(".nav-links");
  if (toggle && links) {
    toggle.addEventListener("click", () => links.classList.toggle("open"));
    links.querySelectorAll("a").forEach((a) =>
      a.addEventListener("click", () => links.classList.remove("open"))
    );
  }

  // scroll reveal
  const revealEls = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window && revealEls.length) {
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("in");
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12 }
    );
    revealEls.forEach((el) => io.observe(el));
  } else {
    revealEls.forEach((el) => el.classList.add("in"));
  }

  // lightbox
  const lightbox = document.querySelector(".lightbox");
  const lightboxImg = lightbox ? lightbox.querySelector("img") : null;
  const closeBtn = lightbox ? lightbox.querySelector(".lightbox-close") : null;

  document.querySelectorAll(".gallery-photo[data-full]").forEach((el) => {
    el.addEventListener("click", () => {
      if (!lightbox || !lightboxImg) return;
      lightboxImg.src = el.dataset.full;
      lightboxImg.alt = el.dataset.alt || "";
      lightbox.classList.add("open");
    });
  });

  const closeLightbox = () => lightbox && lightbox.classList.remove("open");
  if (closeBtn) closeBtn.addEventListener("click", closeLightbox);
  if (lightbox) {
    lightbox.addEventListener("click", (e) => {
      if (e.target === lightbox) closeLightbox();
    });
  }
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") closeLightbox();
  });

  // custom event tooltips
  const tipEls = document.querySelectorAll(".event-tip[data-tip]");
  if (tipEls.length) {
    const tooltip = document.createElement("div");
    tooltip.className = "custom-tooltip";
    document.body.appendChild(tooltip);

    const showTip = (el) => {
      tooltip.textContent = el.dataset.tip;
      tooltip.classList.add("show");
      const rect = el.getBoundingClientRect();
      const tipRect = tooltip.getBoundingClientRect();
      let left = rect.left + rect.width / 2 - tipRect.width / 2;
      left = Math.max(8, Math.min(left, window.innerWidth - tipRect.width - 8));
      let top = rect.top - tipRect.height - 10;
      if (top < 8) top = rect.bottom + 10;
      tooltip.style.left = left + "px";
      tooltip.style.top = top + "px";
    };
    const hideTip = () => tooltip.classList.remove("show");

    tipEls.forEach((el) => {
      el.setAttribute("tabindex", "0");
      el.addEventListener("mouseenter", () => showTip(el));
      el.addEventListener("mouseleave", hideTip);
      el.addEventListener("focus", () => showTip(el));
      el.addEventListener("blur", hideTip);
    });

    window.addEventListener("scroll", hideTip, { passive: true });
  }
});
