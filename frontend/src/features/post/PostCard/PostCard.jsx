import style from './style.module.css'

function PostCard({authorname, posttitle, postdescription="", img_list=[]}){
    return (
        <div className={style.postcard}>
            <div className={style.postheading}>
                <div className={style.postauthor}>
                    <span className={style.authorname}>{authorname}</span>
                </div>
                <button>close</button>
            </div>
            <div className={style.postcontent}>
                <div className={style.posttitle}>{posttitle}</div>
                <div className={style.postdescription}>{postdescription}</div>
                {img_list.map((img_data)=>
                (<div className="postimage">
                    <img src={img_data.url} alt="" />
                </div>)
                )}
            </div>
            <div className={style.postfooter}>
                <div className={style.reactionbuttons}>
                    <button>Like</button>
                    <button>Comment</button>
                    <button>Share</button>
                </div>
                <div className={style.totalreactions}>
                    <span>10 Likes</span>
                    <span>2 Comments</span>
                    <span>0 Shares</span>
                </div>
            </div>
        </div>
    )
}

export {PostCard}