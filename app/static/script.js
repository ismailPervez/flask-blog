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