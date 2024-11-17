from manim import *

class RefinedSequenceDiagram(Scene):
    def construct(self):
        # Define participant labels (Client, Server, Database)
        client = Text("Client", color=WHITE).to_edge(LEFT)
        server = Text("Server", color=WHITE).to_edge(UP)
        database = Text("Database", color=WHITE).to_edge(RIGHT)

        # Display the participants
        self.play(FadeIn(client), FadeIn(server), FadeIn(database))
        self.wait(1)

        # Draw lifelines
        client_line = Line(client.get_bottom(), client.get_bottom() + DOWN * 5)
        server_line = Line(server.get_bottom(), server.get_bottom() + DOWN * 5)
        database_line = Line(database.get_bottom(), database.get_bottom() + DOWN * 5)

        self.play(Create(client_line), Create(server_line), Create(database_line))
        self.wait(1)

        # Define helper function for sequence step
        def sequence_step(start_obj, end_obj, text, color):
            arrow = Arrow(
                start=start_obj.get_right(), 
                end=end_obj.get_left(), 
                buff=0.5, 
                color=color
            )
            label = Text(text, font_size=24, color=color).next_to(arrow, UP)
            glow_arrow = arrow.copy().set_stroke(width=10, opacity=0.3).set_color(YELLOW)
            
            self.play(Create(glow_arrow), Create(arrow), Write(label))
            self.wait(1)
            self.play(FadeOut(arrow), FadeOut(glow_arrow), FadeOut(label))

        # Sequence 1: Client -> Server
        sequence_step(client, server, "Request", BLUE)

        # Sequence 2: Server -> Database
        sequence_step(server, database, "Forward", GREEN)

        # Sequence 3: Database -> Server
        sequence_step(database, server, "Response", YELLOW)

        # Sequence 4: Server -> Client
        sequence_step(server, client, "Response", RED)

        # Hold the final image for a while
        self.wait(2)
