with tab4:
        df = st.session_state.df

        # Make sure it's not empty
        if not df.empty:
            # Sum of Amounts per Predicted Account
            account_summary = df.groupby("Predicted Account")["Amount"].sum().reset_index()
            account_summary.columns = ["Predicted Account", "Total Amount"]

            # Histogram of Amounts
            fig = px.histogram(
                df,
                x="Amount",
                nbins=30,
                marginal="box",
                title="Transaction Amount Distribution",
            )
            fig.update_layout(
                xaxis_title="Amount",
                yaxis_title="Frequency",
                bargap=0.1,
            )
            st.plotly_chart(fig, use_container_width=True)

            account_summary_abs = df.groupby("Predicted Account")["Amount"].apply(lambda x: x.abs().sum()).reset_index()
            account_summary_abs.columns = ["Predicted Account", "Total Amount"]

            fig = px.pie(
            account_summary_abs,
            names="Predicted Account",
            values="Total Amount",
            title="Total Amount per Predicted Account (Absolute Values)",
            hole=0.4
                )
            st.plotly_chart(fig, use_container_width=True)

            # Bar chart (sums instead of counts)
            fig = px.bar(
                account_summary,
                x="Predicted Account",
                y="Total Amount",
                title="Total Amount by Predicted Account",
                text="Total Amount",
                color="Predicted Account"
            )
            fig.update_layout(
                xaxis_title="Predicted Account",
                yaxis_title="Total Amount",
                showlegend=False
            )
            df = st.session_state.df
            st.plotly_chart(fig, use_container_width=True)
            df['Date'] = pd.to_datetime(df['Date'])

            # Sum amount per day
            daily_expenses = df.groupby('Date')['Amount'].sum().reset_index()

            fig = px.line(
                    daily_expenses,
                    x='Date',
                    y='Amount',
                    title='Expenses Over Time',
                    markers=True
                )
            fig.update_layout(
                    xaxis_title='Date',
                    yaxis_title='Total Daily Expenses',
                )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data available for analytics. Please upload and process a file first.")