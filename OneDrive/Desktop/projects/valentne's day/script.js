/* Confetti Effect (kept global for inline handlers) */
function confetti(){
    for(let i=0;i<100;i++){
        let conf=document.createElement('div');
        conf.style.position="fixed";
        conf.style.width="10px";
        conf.style.height="10px";
        conf.style.background="hsl("+Math.random()*360+",100%,50%)";
        conf.style.left=Math.random()*100+"%";
        conf.style.top="-10px";
        conf.style.opacity="0.8";
        conf.style.transform="rotate("+Math.random()*360+"deg)";
        conf.style.animation="fall 3s linear forwards";
        document.body.appendChild(conf);
        setTimeout(()=>conf.remove(),3000);
    }
}

/* YES Button (kept global for inline handlers) */
function sayYes(){
    const msg = document.getElementById("loveMessage");
    if (msg) msg.style.display = "block";
    confetti();
}
// Ensure global access if script type/module or strict scoping
window.sayYes = sayYes;

/* Initialize features after DOM is ready to avoid null reference errors */
document.addEventListener('DOMContentLoaded', () => {
    /* Fade In on Scroll */
    const targets = document.querySelectorAll('.hero, section');
    if ('IntersectionObserver' in window) {
        const observer = new IntersectionObserver(entries => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('show');
                    observer.unobserve(entry.target);
                }
            });
        });
        targets.forEach(el => observer.observe(el));
    } else {
        // Fallback for older browsers
        targets.forEach(el => el.classList.add('show'));
    }

    /* Floating Hearts */
    const heartsContainer = document.querySelector('.hearts');
    if (heartsContainer) {
        for (let i = 0; i < 20; i++) {
            const heart = document.createElement('span');
            heart.innerHTML = "❤️";
            heart.style.left = Math.random() * 100 + "%";
            heart.style.fontSize = Math.floor(Math.random() * 20 + 15) + "px";
            heart.style.animationDuration = (Math.random() * 5 + 5) + "s";
            heartsContainer.appendChild(heart);
        }
    }

    /* Typing Effect */
    const text = "From the moment we met, my life changed forever. Your smile, your laughter, your warmth — everything about you makes my world brighter. I promise to stand by you through every moment of life.";
    const typedEl = document.getElementById("typedText");
    if (typedEl) {
        let index = 0;
        const type = () => {
            if (index < text.length) {
                typedEl.innerHTML += text.charAt(index);
                index++;
                setTimeout(type, 40);
            }
        };
        type();
    }

    /* NO Button Escape */
    const noBtn = document.getElementById("noBtn");
    if (noBtn) {
        const moveBtn = () => {
            const x = Math.random() * (window.innerWidth - noBtn.offsetWidth);
            const y = Math.random() * (window.innerHeight - noBtn.offsetHeight);
            noBtn.style.position = "fixed";
            noBtn.style.left = Math.max(0, x) + "px";
            noBtn.style.top = Math.max(0, y) + "px";
        };
        noBtn.addEventListener("mouseover", moveBtn);
        noBtn.addEventListener("touchstart", (e) => { e.preventDefault(); moveBtn(); }, { passive: false });
    }
});
