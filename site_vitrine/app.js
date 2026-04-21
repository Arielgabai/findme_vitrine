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

const contactStatus = new URLSearchParams(window.location.search).get("contact");
const contactStatusElement = document.querySelector(".form-status");

if (contactStatusElement && contactStatus) {
    const statusMessages = {
        success: {
            type: "is-success",
            text: "Votre demande a bien ete envoyee. Nous reviendrons vers vous rapidement par e-mail."
        },
        invalid: {
            type: "is-error",
            text: "Merci de verifier les champs obligatoires du formulaire avant de l'envoyer."
        },
        error: {
            type: "is-error",
            text: "L'envoi n'a pas pu aboutir pour le moment. Vous pouvez reessayer ou nous ecrire directement a ariel.gabai@hotmail.fr."
        },
        config: {
            type: "is-error",
            text: "Le formulaire n'est pas encore configure pour l'envoi d'e-mails. Renseignez les variables SMTP du site vitrine pour l'activer."
        }
    };

    const selectedStatus = statusMessages[contactStatus];

    if (selectedStatus) {
        contactStatusElement.textContent = selectedStatus.text;
        contactStatusElement.classList.add("is-visible", selectedStatus.type);
    }
}
