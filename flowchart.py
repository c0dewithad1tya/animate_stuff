from manim import *

class PaymentFlowDiagram(Scene):
    def construct(self):
        # Define font and opacity
        font = "Courier New"
        node_opacity = 0.2
        text_opacity = 0.85
        subtext_font_size = 12  # Smaller font size for subtext
        label_font_size = 16    # Smaller font size for main labels
        flow_font_size = 14     # Smaller font size for transition labels

        # Create the nodes and start from top-left corner
        ux = RoundedRectangle(width=3, height=1, color=BLUE).shift(UP * 2.5 + LEFT * 4).set_fill(BLUE, opacity=node_opacity)
        ux_label = Text("UX", font=font, font_size=label_font_size, weight=BOLD).move_to(ux.get_center())

        domain_api = RoundedRectangle(width=4, height=1, color=GREEN).next_to(ux, RIGHT, buff=2).set_fill(GREEN, opacity=node_opacity)
        domain_api_label = Text("Domain API Layer", font=font, font_size=label_font_size, weight=BOLD).move_to(domain_api.get_center())

        microvalidator = RoundedRectangle(width=5, height=1, color=YELLOW).next_to(domain_api, RIGHT, buff=2).set_fill(YELLOW, opacity=node_opacity)
        microvalidator_label = Text("MicroValidator API", font=font, font_size=label_font_size, weight=BOLD).move_to(microvalidator.get_center())

        ftm = RoundedRectangle(width=3, height=1, color=RED).next_to(microvalidator, RIGHT, buff=2).set_fill(RED, opacity=node_opacity)
        ftm_label = Text("FTM", font=font, font_size=label_font_size, weight=BOLD).move_to(ftm.get_center())

        # Add nodes and labels
        self.play(FadeIn(ux), Write(ux_label))
        self.play(FadeIn(domain_api), Write(domain_api_label))
        self.play(FadeIn(microvalidator), Write(microvalidator_label))
        self.play(FadeIn(ftm), Write(ftm_label))
        self.wait(1)

        # Transition arrows and text
        def add_flow(start, end, label_text, color):
            arrow = Arrow(start=start.get_bottom(), end=end.get_top(), buff=0.5, color=color, stroke_width=3)
            label = Text(label_text, font=font, font_size=flow_font_size, weight=BOLD).next_to(arrow, RIGHT, buff=0.2).set_opacity(text_opacity)

            # Create glow effect
            glow_arrow = arrow.copy().set_stroke(width=10, opacity=0.3).set_color(YELLOW)
            self.play(Create(glow_arrow), Create(arrow), Write(label))
            self.wait(1)
            self.play(FadeOut(glow_arrow))

        # Add transition arrows between main stages
        add_flow(ux, domain_api, "Customer enters payment info", BLUE)
        add_flow(domain_api, microvalidator, "Validation & request to MicroValidator", GREEN)
        add_flow(microvalidator, ftm, "Send pain.001 to FTM", YELLOW)

        # MicroValidator internal service calls: Display each service one by one
        services = [
            "DebtorAccEnrich", "AccessTypeLookup", "CreditorAccEnrich",
            "IbanLookup", "ValidateBBAN", "TransactionIdentificationControl",
            "CutoffBD", "TransactionExecutionService"
        ]

        # Create and animate each service node inside MicroValidator
        service_nodes = VGroup()
        for i, service in enumerate(services):
            service_node = RoundedRectangle(width=4, height=0.6, color=ORANGE).set_fill(ORANGE, opacity=node_opacity)
            service_label = Text(service, font=font, font_size=subtext_font_size).move_to(service_node.get_center())
            service_node_group = VGroup(service_node, service_label).next_to(microvalidator, DOWN, buff=1.5 + (i * 1.2))

            service_nodes.add(service_node_group)

        # Animate services one by one with fade in and fade out
        for service_node in service_nodes:
            self.play(FadeIn(service_node))
            self.wait(0.5)
            self.play(FadeOut(service_node))
        self.wait(1)

        # FTM steps
        ftm_steps = [
            ("Map pain.001", RED),
            ("Validation via lookup service", YELLOW),
            ("Wait for customer approval", RED)
        ]

        # Show FTM steps in a new line after MicroValidator services
        for i, (step, color) in enumerate(ftm_steps):
            step_box = RoundedRectangle(width=4.5, height=0.8, color=color).set_fill(color, opacity=node_opacity)
            step_label = Text(step, font=font, font_size=subtext_font_size).move_to(step_box.get_center())
            step_box_group = VGroup(step_box, step_label).next_to(ftm, DOWN, buff=1.5 + (i * 1.2))

            # Animate each step of FTM
            self.play(FadeIn(step_box_group))
            self.wait(1)

        # Hold the final frame
        self.wait(2)
