import { PostCard } from "../PostCard/PostCard"
import style from './style.module.css'
import { GET_ALL_POSTS } from "../graphql/postsQueries";
import { useQuery } from "@apollo/client/react";

function PostList(){
    const { data, loading, error } = useQuery(GET_ALL_POSTS);
    console.log(data)
    if (loading) return <div className={style.postcontainer}>Loading Posts...</div>;
    if (error) return <div className="text-red-500">Error! {error.message}</div>;
    return (
        <>
            {data.allUserPosts.edges.map((edge)=>
                (
                    <div className={style.postcontainer}>
                        <PostCard 
                        authorname={edge.node.createdBy.name} 
                        posttitle={edge.node.title}
                        postdescription={edge.node.description}
                        img_list={[
                            {url: "static/images/506302782_9643445375778926_6296838114955530405_n.jpg"}
                        ]}
                        />
                    </div>
                )
            )}
        </>
    )
}

export {PostList}