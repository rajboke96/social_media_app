import { PostCard } from "../PostCard/PostCard"
import style from '../PostList/style.module.css'
import { GET_USER_FEED } from "../graphql/feedQueries";
import { useQuery } from "@apollo/client/react";

function FeedList(){
    const { data, loading, error } = useQuery(GET_USER_FEED, {
        variables: { first: 20 }
    });
    
    if (loading) return <div className={style.postcontainer}>Loading your personalized feed...</div>;
    if (error) return <div className="text-red-500">Error loading feed! {error.message}</div>;
    
    if (!data?.getFeedsForUser?.edges || data.getFeedsForUser.edges.length === 0) {
        return (
            <div className={style.postcontainer}>
                <p style={{ textAlign: 'center', color: '#9ca3af', padding: '2rem' }}>
                    No posts to show. Follow more users to see their posts!
                </p>
            </div>
        );
    }

    return (
        <>
            {data.getFeedsForUser.edges.map((edge)=>
                (
                    <div key={edge.node.id} className={style.postcontainer}>
                        <PostCard 
                        authorname={edge.node.createdBy.name || edge.node.createdBy.username} 
                        posttitle={edge.node.title}
                        postdescription={edge.node.description}
                        postId={edge.node.id}
                        img_list={
                            edge.node.media?.length > 0 
                                ? edge.node.media.map(m => ({ url: m.feedUrl || m.url }))
                                : [{ url: "static/images/506302782_9643445375778926_6296838114955530405_n.jpg" }]
                        }
                        />
                    </div>
                )
            )}
        </>
    )
}

export { FeedList }
