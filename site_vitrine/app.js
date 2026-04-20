const menuToggle = document.querySelector(".menu-toggle");
const nav = document.querySelector(".nav");

if (menuToggle && nav) {
    menuToggle.addEventListener("click", () => {
        const isOpen = nav.classList.toggle("open");
        menuToggle.setAttribute("aria-expanded", String(isOpen));
    });

    nav.querySelectorAll("a").forEach((link) => {
        link.addEventListener("click", () => {
            nav.classList.remove("open");
            menuToggle.setAttribute("aria-expanded", "false");
        });
    });
}

document.querySelectorAll(".faq-question").forEach((button) => {
    button.addEventListener("click", () => {
        const item = button.closest(".faq-item");
        if (!item) return;

        item.classList.toggle("open");
    });
});

const revealTargets = document.querySelectorAll(
    ".hero-copy, .hero-visual, .proof-strip article, .section-heading, .value-card, .feature-card, .timeline-step, .comparison-card, .faq-item, .cta-card"
);

const revealObserver = new IntersectionObserver(
    (entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                entry.target.classList.add("reveal", "is-visible");
            }
        });
    },
    {
        threshold: 0.15
    }
);

revealTargets.forEach((element) => {
    element.classList.add("reveal");
    revealObserver.observe(element);
});
