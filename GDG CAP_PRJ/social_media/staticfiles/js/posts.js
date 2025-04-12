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