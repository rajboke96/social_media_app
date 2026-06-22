from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from social_media_app.schemas import Post, User, Friend, Like, Comment, PostView, UserRole, Visibility, FriendRequestStatus
from datetime import datetime, timedelta
from src.logger import get_logger

logger = get_logger(__name__)


async def get_user_feed(db: AsyncSession, user_id: int, limit: int = 20, offset: int = 0):
    """
    Generate a personalized feed for a user based on:
    1. Posts from followed users (accepted friends)
    2. User's own posts
    3. Posts sorted by relevance score (likes, comments, recency)
    """
    
    try:
        # Get list of users that current user follows (accepted friends)
        friends_statement = (
            select(Friend.friend_id)
            .where(
                and_(
                    Friend.user_id == user_id,
                    Friend.status == FriendRequestStatus.ACCEPTED
                )
            )
        )
        friends_result = await db.execute(friends_statement)
        friend_ids = [row[0] for row in friends_result.all()]

        # Get IDs of posts that the user has already seen
        seen_statement = (
            select(PostView.post_id)
            .where(PostView.user_id == user_id)
        )
        seen_result = await db.execute(seen_statement)
        seen_post_ids = [row[0] for row in seen_result.all()]

        # Build engagement subqueries once
        like_count_subquery = (
            select(Like.post_id, func.count(Like.id).label('like_count'))
            .group_by(Like.post_id)
            .subquery()
        )

        comment_count_subquery = (
            select(Comment.post_id, func.count(Comment.id).label('comment_count'))
            .group_by(Comment.post_id)
            .subquery()
        )

        age_threshold = datetime.utcnow() - timedelta(days=7)
        age_formula = func.datediff(func.now(), Post.created_at)

        def build_feed_query(post_ids_filter=None, public_only=False):
            filters = []
            if post_ids_filter is not None:
                filters.append(Post.id.notin_(post_ids_filter))
            if public_only:
                filters.append(Post.visibility == Visibility.PUBLIC)
            else:
                filters.append(Post.visibility.in_([Visibility.PUBLIC, Visibility.FRIENDS]))

            return (
                select(
                    Post,
                    func.coalesce(like_count_subquery.c.like_count, 0).label('like_count'),
                    func.coalesce(comment_count_subquery.c.comment_count, 0).label('comment_count')
                )
                .join(like_count_subquery, Post.id == like_count_subquery.c.post_id, isouter=True)
                .join(comment_count_subquery, Post.id == comment_count_subquery.c.post_id, isouter=True)
                .where(*filters)
                .where(Post.created_at >= age_threshold)
                .options(selectinload(Post.user), selectinload(Post.media))
                .order_by(
                    (
                        func.coalesce(like_count_subquery.c.like_count, 0) +
                        (func.coalesce(comment_count_subquery.c.comment_count, 0) * 2) -
                        (age_formula / 24)
                    ).desc(),
                    Post.created_at.desc()
                )
                .offset(offset)
                .limit(limit)
            )

        if len(friend_ids) == 0:
            # New user with no followers: show best public posts
            statement = build_feed_query(post_ids_filter=seen_post_ids, public_only=True)
            result = await db.execute(statement)
            posts = result.unique().scalars().all()
        else:
            # Regular feed: only show posts from friends + self, excluding seen posts
            statement = build_feed_query(post_ids_filter=seen_post_ids)
            statement = statement.where(Post.created_by.in_(friend_ids + [user_id]))
            result = await db.execute(statement)
            posts = result.unique().scalars().all()

            if len(posts) == 0:
                # Fallback: if there are no new friend posts, show best public posts not seen
                fallback_statement = build_feed_query(post_ids_filter=seen_post_ids, public_only=True)
                result = await db.execute(fallback_statement)
                posts = result.unique().scalars().all()

        logger.info(f'exit get_user_feed: fetched {len(posts)} posts for user {user_id}')
        return posts
        
    except Exception as e:
        logger.error(f'Error in get_user_feed: {str(e)}')
        raise
