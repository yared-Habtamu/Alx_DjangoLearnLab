// Enhanced like functionality with error handling
document.addEventListener('DOMContentLoaded', function() {
    // Like/Unlike posts
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('like-btn')) {
            e.preventDefault();
            const button = e.target;
            const postId = button.dataset.postId;
            const action = button.dataset.action;
            const url = `/posts/${postId}/${action}/`;
            
            button.disabled = true;
            button.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
            
            fetch(url, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json'
                },
                credentials: 'same-origin'
            })
            .then(response => {
                if (!response.ok) throw new Error('Network response was not ok');
                return response.json();
            })
            .then(data => {
                if (data.error) throw new Error(data.error);
                
                // Update button state
                const newAction = action === 'like' ? 'unlike' : 'like';
                button.dataset.action = newAction;
                button.innerHTML = newAction === 'like' ? 
                    '<i class="far fa-thumbs-up"></i> Like' : 
                    '<i class="fas fa-thumbs-up"></i> Unlike';
                
                // Update like count
                const likeCount = button.nextElementSibling;
                if (likeCount.classList.contains('like-count')) {
                    const currentCount = parseInt(likeCount.textContent);
                    likeCount.textContent = action === 'like' ? currentCount + 1 : currentCount - 1;
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Failed to process like: ' + error.message);
            })
            .finally(() => {
                button.disabled = false;
            });
        }
    });
});
// Handle like actions
document.querySelectorAll('.like-form').forEach(form => {
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const postId = this.dataset.postId;

        fetch(this.action, {
            method: 'POST',
            headers: {
                'X-CSRFToken': this.querySelector('[name=csrfmiddlewaretoken]').value,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({})
        })
        .then(response => response.json())
        .then(data => {
            if(data.status === 'ok') {
                const likeBtn = this.querySelector('.like-btn');
                const likeCount = this.querySelector('.like-count');

                // Update heart icon
                likeBtn.innerHTML = `<i class="${data.liked ? 'fas' : 'far'} fa-heart"></i>`;
                likeCount.textContent = data.total_likes;
            }
        });
    });
});

// Handle comment submission
document.querySelectorAll('.comment-form').forEach(form => {
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const textarea = this.querySelector('textarea');

        fetch(this.action, {
            method: 'POST',
            headers: {
                'X-CSRFToken': this.querySelector('[name=csrfmiddlewaretoken]').value,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                content: textarea.value
            })
        })
        .then(response => response.json())
        .then(data => {
            if(data.status === 'ok') {
                const commentsList = document.querySelector('.comments-list');
                const newComment = document.createElement('div');

                newComment.className = 'comment';
                newComment.innerHTML = `
                    <div class="comment-header">
                        <img src="${data.avatar}" class="comment-avatar">
                        <a href="/user/${data.user_id}/">${data.username}</a>
                        <span class="comment-date">Just now</span>
                    </div>
                    <div class="comment-content">${data.content}</div>
                `;

                // Add new comment to top
                commentsList.insertBefore(newComment, commentsList.firstChild);
                textarea.value = '';

                // Update comment count
                document.querySelector('.comment-count').textContent =
                    `${data.total_comments} comments`;
            }
        });
    });
});