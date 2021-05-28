document.addEventListener('DOMContentLoaded', function () {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');

  document.querySelector('#compose-form').onsubmit = () => {

    // Create new item for list
    
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
        recipients: document.querySelector("#compose-recipients").value,
        subject: document.querySelector("#compose-subject").value,
        body: document.querySelector("#compose-body").value,
      })
    })
    .then(response => response.json())
    .then(result => {
      // Print result
      console.log(result);
      if(result.error){
        document.querySelector("#message").innerHTML=`<span style="color:red">Error:</span> ${result.error}`;
      }
      else{
        load_mailbox('sent');
        document.querySelector("#message").innerHTML=`<span style="font-weight: bold;">Message:</span> ${result.message}`;
      }
      
    });
    

    return false;
};


});






function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  if(mailbox==="sent"){
    fetch('/emails/sent')
    .then(response => response.json())
    .then(emails => {
    // Print emails
    console.log(emails);
    // ... do something else with emails ...

    });
  }
  if(mailbox==="inbox"){
    fetch('/emails/inbox')
    .then(response => response.json())
    .then(emails => {
    // Print emails
    //console.log(emails);
    var i;
    for(i=0; i<emails.length;i++){
      var ele= document.createElement("div");
      ele.innerHTML="TEST";
      ele.addEventListener('click',function(){
        console.log(i);
      });
      document.querySelector('.container').append(ele);

    }
    // ... do something else with emails ...
    });
  }

  if(mailbox==="archive"){
    fetch('/emails/archive')
    .then(response => response.json())
    .then(emails => {
    // Print emails
    console.log(emails);

    // ... do something else with emails ...
    });
  }

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
}