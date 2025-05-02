import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import base64

def main():
    # Load and base64-encode the background image
    with open("2sd1.jpg", "rb") as img_file:
        b64_img = base64.b64encode(img_file.read()).decode()

    # Inject CSS: background + white title & markdown paragraphs + white <hr>
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url("data:image/jpeg;base64,{b64_img}") no-repeat center center fixed;
            background-size: cover;
        }}
        /* White for h1 and markdown paragraphs */
        h1, .markdown-text-container p {{
            color: white !important;
            text-shadow: 1px 1px 4px rgba(0,0,0,0.8);
        }}
        /* Make <hr> lines white */
        hr {{
            border: none;
            border-top: 1px solid white !important;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Centered title
    st.markdown("<h1>Static Visualization Task 1</h1>", unsafe_allow_html=True)

    # Load and clean the data
    coffee_df = pd.read_csv("simplified_coffee.csv")
    coffee_df["100g_USD"] = pd.to_numeric(coffee_df["100g_USD"], errors="coerce")
    coffee_df["rating"]   = pd.to_numeric(coffee_df["rating"],   errors="coerce")
    coffee_df.dropna(subset=["100g_USD", "rating"], inplace=True)

    # Create price bins and labels
    bins   = [0, 10, 20, 30, 40, 50, 100, float("inf")]
    labels = ["0-10", "10-20", "20-30", "30-40", "40-50", "50-100", "100+"]
    coffee_df["price_range"] = pd.cut(coffee_df["100g_USD"], bins=bins, labels=labels)

    # Calculate average ratings
    avg_ratings = coffee_df.groupby("price_range")["rating"].mean()

    # Plot
    fig, ax = plt.subplots(figsize=(10, 6))
    avg_ratings.plot(
        kind="bar",
        color=(229/255, 152/255, 102/255, 0.8),
        edgecolor="black",
        ax=ax
    )

    # Chart styling (default dark text)
    ax.set_title("Average Coffee Rating by Price Range", fontsize=16, pad=20, fontweight="bold")
    ax.set_xlabel("Price Range per 100g (USD)", fontsize=12, labelpad=10, fontweight="bold")
    ax.set_ylabel("Average Rating", fontsize=12, labelpad=10, fontweight="bold")
    ax.set_ylim(90, 96)
    ax.grid(False)
    ax.tick_params(axis="x", rotation=0)
    ax.set_xticklabels(labels, fontweight="bold")
    ax.set_yticklabels([str(int(t)) for t in ax.get_yticks()], fontweight="bold")

    # Value labels inside bars
    for i, v in enumerate(avg_ratings):
        ax.text(i, v + 0.05, f"{v:.1f}", ha="center", va="bottom",
                fontsize=12, fontweight="bold")

    # Display the plot
    st.pyplot(fig)

    # White centered bullet annotations with white line above
    st.markdown('<hr/>', unsafe_allow_html=True)
    st.markdown(
        """
        <div style="text-align: center;">
          <ul style="
              display: inline-block;
              text-align: left;
              color: white;
              font-weight: bold;
              padding-left: 1em;
              margin: 0;
          ">
            <li>The highest price range (100+ USD) has the highest average rating of 95.0.</li>
            <li>The lowest price range (0-10 USD) has the lowest average rating of 93.1.</li>
            <li>The average ratings rise with higher prices, particularly from the 20-30 USD price range and above.</li>
          </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

if __name__ == "__main__":
    main()
