// upvote and downvote functions
var upvoteBtns = document.querySelectorAll('.fa-thumbs-up')
var downvoteBtns = document.querySelectorAll('.fa-thumbs-down')

// upvoting
upvoteBtns.forEach(upvote_btn => {
    upvote_btn.addEventListener('click', (event) => {
        var post = event.target.parentElement.parentElement.parentElement
        var voteCountContainer = post.querySelector(".upvote-count")
        var voteCount = parseInt(post.querySelector(".upvote-count").textContent)
        voteCount += 1
        voteCountContainer.textContent = voteCount
        var post_id = parseInt(post.id.split('-')[1])
        
        fetch(`/update/${post_id}`, {
            method: "PUT",
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                "upvotes": voteCount
            })
        })     
    })
})

// downvoting
downvoteBtns.forEach(downvote_btn => {
    downvote_btn.addEventListener('click', (event) => {
        var post = event.target.parentElement.parentElement.parentElement
        var voteCountContainer = post.querySelector(".downvote-count")
        var voteCount = parseInt(post.querySelector(".downvote-count").textContent)
        voteCount += 1
        voteCountContainer.textContent = voteCount
        var post_id = parseInt(post.id.split('-')[1])
        
        fetch(`/update/${post_id}`, {
            method: "PUT",
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                "downvotes": voteCount
            })
        })     
    })
})

// toggle menu 
var toggleMenuBtn = document.querySelector("header .fa-bars")
var menu  = document.querySelector(".menu-container")
var closeMenuBtn = document.querySelector(".menu-container .fa-times")

// var menuStatus = false
toggleMenuBtn.addEventListener("click", (event) => {
    menu.classList.add("active")
})

closeMenuBtn.addEventListener("click", () => {
    menu.classList.remove("active")
})

// // get quote
// window.onload = () => {
//     const quote = document.getElementById('quote')
//     const author = document.getElementById('author')
//     fetch('http://quotes.stormconsultancy.co.uk/random.json')
//         .then(res => res.json())
//         .then(data => {
//             quote.textContent = data.quote
//             author.textContent = data.author
//         })
// }