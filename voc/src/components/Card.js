import React from "react"

import RatingButtons from "./RatingButtons"
import styles from "./Card.module.css"

class Card extends React.Component {
    render() {
        const { uid, word, rating, count} = this.props.entry
        return (
            <div
                id={uid}
                className={styles.container}
            >
                <div className={styles.word}>{word}</div>
                {console.log(rating, count)}
                <br/>
                <RatingButtons 
                    // className={styles.ratingButtons}
                    word={word}
                    rateWordProps={this.props.rateWordProps}
                />
            </div>
        )
    }
}

export default Card