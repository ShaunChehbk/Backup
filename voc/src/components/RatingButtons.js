import React from "react"
import styles from "./Button.module.css"

class RatingButtons extends React.Component {
    ratings = [1, 2, 3, 4, 5]
    state = {
        touched : false
    }
    render() {
        return (
            <div className={this.state.touched ? styles.hidden : styles.ratingButtons }>
                {this.ratings.map(rating => (
                    <button
                        className={styles.button}
                        key={rating}
                        onClick={() => {
                            this.setState({touched: true})
                            this.props.rateWordProps(this.props.word, rating)
                        }}
                    >
                        {rating}
                    </button>
                ))}
            </div>
        )
    }
}
export default RatingButtons