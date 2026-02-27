// slider logic moved from head
(function(){
  document.querySelectorAll("[data-ba]").forEach((wrap) => {
    const range = wrap.querySelector(".ba-range");
    const afterWrap = wrap.querySelector(".ba-afterWrap");
    if (!range || !afterWrap) return;

    const update = () => {
      const v = Number(range.value || 50);
      afterWrap.style.width = v + "%";
      wrap.style.setProperty("--baLinePos", v + "%");
    };

    range.addEventListener("input", update);
    update();
  });
})();

// page scripting
(function(){
  document.getElementById("yr").textContent = new Date().getFullYear();

  // Mobile menu
  const burger = document.getElementById("burger");
  const menu = document.getElementById("mobileMenu");
  burger?.addEventListener("click", () => {
    const open = menu.style.display === "block";
    menu.style.display = open ? "none" : "block";
  });
  menu?.querySelectorAll("a").forEach(a => a.addEventListener("click", () => menu.style.display = "none"));

  // UTM capture
  const params = new URLSearchParams(window.location.search);
  ["utm_source","utm_campaign","utm_term","utm_content"].forEach(k => {
    const el = document.getElementById(k);
    if (el) el.value = params.get(k) || "";
  });

  // 2-step form logic (micro-commitment)
  const stepNum = document.getElementById("stepNum");
  const barFill = document.getElementById("barFill");
  const step1 = document.getElementById("step1");
  const step2 = document.getElementById("step2");
  const nextBtn = document.getElementById("nextBtn");
  const backBtn = document.getElementById("backBtn");
  const successBox = document.getElementById("successBox");
  const leadForm = document.getElementById("leadForm");

  function showStep(n){
    const isStep1 = (n === 1);
    step1.classList.toggle("active", isStep1);
    step2.classList.toggle("active", !isStep1);
    stepNum.textContent = isStep1 ? "1" : "2";
    barFill.classList.toggle("done", !isStep1);
  }

  nextBtn?.addEventListener("click", () => {
    const facility = document.getElementById("facility")?.value?.trim();
    const email = document.getElementById("email")?.value?.trim();
    if (!facility) return alert("Please enter the facility name/address.");
    if (!email) return alert("Please enter a work email.");
    showStep(2);
  });

  backBtn?.addEventListener("click", () => showStep(1));

  // IMPORTANT: Replace `endpoint` with your real handler.
  // If you use a webhook (GHL), add it here and map the fields on the receiving side.
  const endpoint = ""; // e.g. "https://hooks.yourcrm.com/lead"

  leadForm?.addEventListener("submit", async (e) => {
    e.preventDefault();

    // Basic HTML validation
    const phone = document.getElementById("phone")?.value?.trim();
    const priority = document.getElementById("priority")?.value;
    if (!phone) return alert("Please enter a mobile number.");
    if (!priority) return alert("Please select the most urgent need.");

    // If no endpoint is set, show success (dev mode)
    if (!endpoint){
      leadForm.style.display = "none";
      successBox.style.display = "block";
      return;
    }

    const formData = new FormData(leadForm);

    try{
      const res = await fetch(endpoint, {
        method: "POST",
        body: formData
      });
      if (!res.ok) throw new Error("Bad response");
      leadForm.style.display = "none";
      successBox.style.display = "block";
    }catch(err){
      alert("Submission failed. Please call/text (602) 767-3546.");
    }
  });

  // ===== TESTIMONIALS CAROUSEL =====
  const testimonialTrack = document.getElementById("testimonialTrack");
  const carouselPrevBtn = document.getElementById("carouselPrevBtn");
  const carouselNextBtn = document.getElementById("carouselNextBtn");
  
  if (testimonialTrack && carouselPrevBtn && carouselNextBtn) {
    let position = 0;
    const cardWidth = testimonialTrack.querySelector(".testimonialCard")?.offsetWidth || 0;
    
    const updateCarousel = () => {
      if (testimonialTrack) {
        testimonialTrack.style.transform = `translateX(${position}px)`;
      }
    };

    carouselPrevBtn.addEventListener("click", () => {
      const maxScroll = -Math.max(0, (testimonialTrack.scrollWidth - window.innerWidth + 24));
      position = Math.min(0, position + cardWidth);
      updateCarousel();
    });

    carouselNextBtn.addEventListener("click", () => {
      const maxScroll = -(testimonialTrack.scrollWidth - window.innerWidth + 24);
      position = Math.max(maxScroll, position - cardWidth);
      updateCarousel();
    });
  }

  // ===== PRICING CALCULATOR =====
  const sqftInput = document.getElementById("sqft");
  const servicesSelect = document.getElementById("services");
  const priceRangeDisplay = document.getElementById("priceRange");
  const sqftDisplay = document.getElementById("sqftDisplay");

  const calculatePrice = () => {
    const sqft = Number(sqftInput?.value || 20000);
    const service = servicesSelect?.value || "wash-sweep";
    
    // Per-sqft pricing tiers
    const baseRate = sqft < 10000 ? 0.25 : sqft < 30000 ? 0.20 : 0.15;
    const washCost = sqft * baseRate;
    
    let low, high;
    if (service === "wash") {
      low = washCost * 0.9;
      high = washCost * 1.1;
    } else if (service === "wash-sweep") {
      low = washCost * 1.3;
      high = washCost * 1.5;
    } else {
      low = washCost * 1.8;
      high = washCost * 2.2;
    }

    // Add minimum threshold
    low = Math.max(low, 2000);
    high = Math.max(high, 3000);

    sqftDisplay.textContent = sqft.toLocaleString();
    priceRangeDisplay.textContent = `$${Math.round(low).toLocaleString()} - $${Math.round(high).toLocaleString()}`;
  };

  sqftInput?.addEventListener("input", calculatePrice);
  servicesSelect?.addEventListener("change", calculatePrice);
  document.getElementById("estQuoteBtn")?.addEventListener("click", () => {
    document.getElementById("contact")?.scrollIntoView({ behavior: "smooth" });
  });

  // ===== SCROLL TO TOP BUTTON =====
  const scrollTopBtn = document.getElementById("scrollTopBtn");

  window.addEventListener("scroll", () => {
    if (window.scrollY > 300) {
      scrollTopBtn?.classList.add("show");
    } else {
      scrollTopBtn?.classList.remove("show");
    }
  });

  scrollTopBtn?.addEventListener("click", () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  });

  // Initial calculation
  calculatePrice();
})();
