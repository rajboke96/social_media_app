import { useState } from 'react';
import { useApolloClient } from '@apollo/client/react';
import { FeedList } from "../../features/post";
import PostManager from "../../features/post/PostManager/PostManager";
import CreatePostForm from "../../features/post/CreatePostForm/CreatePostForm";
import Modal from "../../components/Modal/Modal";
import style from "./style.module.css";

function Feeds(){
    const [isModalOpen, setIsModalOpen] = useState(false);
    const client = useApolloClient();

    const handlePostCreated = async () => {
        await client.refetchQueries({ include: 'active' });
        setIsModalOpen(false);
    };

    return (
        <div className={style.feedsPage}>
            <div className={style.createPostPrompt}>
                <button onClick={() => setIsModalOpen(true)} className={style.createPostBtn}>
                    + Create post
                </button>
            </div>
            <FeedList />
            <Modal open={isModalOpen} onClose={() => setIsModalOpen(false)}>
                <CreatePostForm onCreated={handlePostCreated} />
            </Modal>
        </div>
    );
}

export {Feeds};
