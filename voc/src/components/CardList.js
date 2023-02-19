import React from "react"

import Card from "./Card"

class CardList extends React.Component {
    render() {
        return (
            <div>
                {this.props.words.map(entry => (
                    <Card 
                        key={entry.uid}
                        entry={entry}
                        rateWordProps={this.props.rateWordProps}
                    />
                ))}
            </div>
        )
    }
}

export default CardList