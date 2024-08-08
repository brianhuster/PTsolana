


const faqData =  [
  {
    question: 'What are the membership options available?',
    
    answer: `Currently We offer 3 membership types, all monthly payment, SILVER, Which is our standard membership and you get access to the gym room with weights and equipment, GOLD, which is more advanced, on top of the silver membership perks, with Gold you also get access to Sauna and our Courts such as the Basketball Court and in our final membership type DIAMOND, we offer You access to everything we offer.`
  },

  {
    question: 'Can I bring a Guest to the Gym?',

    answer: `Yes, we offer guest passes for a nominal fee. Contact our front desk or check our website for guest pass availablity and rates.`
  },

  {
    question: 'Are personal training sessions included in my membership?',

    answer: `Personal training sessions are not included in our membership plans but can be purchased separately. Contact our reception or via e-mail`
  },

  {
    question: 'What Group fitness classes do you offer?',

    answer: `Our diverse range of classes includes cardio intense programs, structured weightlifting programs, yoga (beginner to advanced), pilates, boxing etc. More information about our Group Programs you can find on the Group Programs page.`
  },

  {
    question: 'How do I sign up for a group training session?',

    answer: `Simply log in to your member portal on our website and view the class schedule and reserve your spot in advance.`
  },

  {
    question: 'Can I sign up to multiple Group sessions in a week?',

    answer: `Of course, just make sure that the group session periods dont overlap, check out the schedule and book your desired sessions today!`
  },

  {
    question: 'What measures are in place for gym cleanliness and hygiene?',

    answer: `We prioritize cleanliness and sanitation, regularly disinfecting equipment and spaces. Hand sanitizing stations are available throughout the gym.`
  },

  {
    question: 'Can I access the gym 24/7?',

    answer: `Yes, we offer 24/7 access to all members of each of the 3 types of memberships we currently offer.`
  },

  {
    question: 'Can I freeze or cancel my membership?',

    answer: `Yes, you can either freeze or cancel your membership at any given moment for a specified period or cancel with proper notice. Refer to our membership terms or contat our customer service for assistance.`
  },

  {
    question: 'Do you offer any special discounts or bonuses?',

    answer: `Yes, we offer great offers such as our refer-a-friend bonus where if you refer a friend of yours, both of you receive a FREE personal training sessions with one of our qualified personal trainers you choose.`
  },

  {
    question: 'Any offers/bonuses for students?',

    answer: `Yes, if you are a student with a valid ID, we offer 10% off on all membership types (silver, gold, diamond) for the first 3 months.`
  },

  {
    question: 'What is the Weekend Warrior Pass?',

    answer: `This is a special event offer  where you have access to the gym room on weekends at a reduced rate.`
  },

  {
    question: 'How can I get notified and updated about your services and offers?',

    answer: `You can do that by signing up to our newsletter on the front page at the bottom.`
  },


];


const faqContainer = document.getElementById('faqs-container');

faqData.map(function(item) {

  let article = document.createElement('article');
  article.className = "faq-item";

  const markup = `
  
    <div class="item-question">
      <span class="question-text cursor">${item.question}</span>
      <span class="expand-close-container">
        <span class="expand"><i class="fa-solid fa-plus"></i></span>
        <span class="close"><i class="fa-solid fa-xmark"></i></span>
      </span>
    </div>

    <div class="item-answer">
      <span class="answer-text">${item.answer}</span>
    </div>
  `;

  article.innerHTML = markup;
  faqContainer.append(article);

});


const expandCloseContainer = document.querySelectorAll('.expand-close-container');

expandCloseContainer.forEach(function(item){

  item.addEventListener('click', function(e){
    const expandIcon = e.currentTarget.parentElement.parentElement;
    expandIcon.classList.toggle('show-answer');

  });

});

const questionText = document.querySelectorAll('.question-text');

questionText.forEach(function(item){

  item.addEventListener('click', function(e){
    const expandQuestion = e.currentTarget.parentElement.parentElement;
    expandQuestion.classList.toggle('show-answer');

  });

});