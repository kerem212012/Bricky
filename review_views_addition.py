


class CreateReviewView(LoginRequiredMixin, CreateView):
    """
    View for creating a product review
    """
    model = Review
    form_class = ReviewForm
    template_name = 'core/create_review.html'
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        """Handle review submission via AJAX"""
        try:
            product_id = request.POST.get('product_id')
            product = get_object_or_404(Product, id=product_id, is_active=True)

            # Check if user already reviewed this product
            if Review.objects.filter(product=product, author=request.user).exists():
                return JsonResponse({
                    'success': False,
                    'message': 'You have already reviewed this product.'
                }, status=400)

            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.product = product
                review.author = request.user
                review.save()

                return JsonResponse({
                    'success': True,
                    'message': 'Review submitted successfully! It will appear after moderation.',
                    'review': {
                        'author': review.author.username,
                        'rating': review.rating,
                        'title': review.title,
                        'content': review.content,
                        'created_at': review.created_at.strftime('%B %d, %Y')
                    }
                })
            else:
                errors = form.errors
                return JsonResponse({
                    'success': False,
                    'message': 'Please fix the errors below.',
                    'errors': errors
                }, status=400)

        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'An error occurred: {str(e)}'
            }, status=500)


class ReviewHelpfulView(LoginRequiredMixin, View):
    """
    AJAX view to mark review as helpful or unhelpful
    """
    def post(self, request, review_id):
        """Handle helpful/unhelpful marking"""
        try:
            review = get_object_or_404(Review, id=review_id)
            action = request.POST.get('action')  # 'helpful' or 'unhelpful'

            if action == 'helpful':
                review.helpful_count += 1
            elif action == 'unhelpful':
                review.unhelpful_count += 1
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Invalid action.'
                }, status=400)

            review.save()

            return JsonResponse({
                'success': True,
                'helpful_count': review.helpful_count,
                'unhelpful_count': review.unhelpful_count
            })

        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'An error occurred: {str(e)}'
            }, status=500)
