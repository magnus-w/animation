#!/usr/bin/env python3
"""
Generate Mars W X-Mas Ornament GIF
"""

import math
import numpy as np
from PIL import Image, ImageDraw
import random

class Point3D:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.rotated_x = x
        self.rotated_y = y
        self.rotated_z = z
        self.projected_2d_x = 0
        self.projected_2d_y = 0

class Line:
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2
        self.color = "#FF6B35"
        self.width = 1
        self.is_artifact = False

class MarsGifGenerator:
    def __init__(self):
        self.canvas_width = 400
        self.canvas_height = 400
        self.radius = min(self.canvas_width, self.canvas_height) * 0.3
        self.center_x = self.canvas_width / 2
        self.center_y = self.canvas_height / 2
        self.latitude_lines = 40
        self.longitude_lines = 48
        self.shading_density = 1200
        self.axial_tilt = 25.19 * math.pi / 180

        # Mars color palette
        self.colors = {
            'light': ['#FF6B35', '#FF8C42', '#FFA552', '#FFB366'],
            'medium': ['#C44536', '#D4573B', '#E06940', '#B43D2F'],
            'dark': ['#8B2E1F', '#6B1F14', '#4A1410', '#2C0D0A'],
            'shadow': ['#1A0806', '#0D0403', '#000000']
        }

        # Initialize geometry
        self.sphere_points = self.create_sphere_points()
        self.structural_lines = self.create_structural_lines()
        self.shading_lines = self.create_shading_lines()
        self.w_artifact = self.create_w_artifact()
        self.all_lines = self.structural_lines + self.shading_lines + self.w_artifact

    def create_sphere_points(self):
        points = []
        for lat in range(self.latitude_lines + 1):
            theta = (lat * math.pi) / self.latitude_lines
            for lon in range(self.longitude_lines + 1):
                phi = (lon * 2 * math.pi) / self.longitude_lines

                x = self.radius * math.sin(theta) * math.cos(phi)
                y = self.radius * math.cos(theta)
                z = self.radius * math.sin(theta) * math.sin(phi)

                points.append(Point3D(x, y, z))
        return points

    def create_structural_lines(self):
        lines = []

        # Latitude lines
        for lat in range(self.latitude_lines + 1):
            for lon in range(self.longitude_lines):
                index = lat * (self.longitude_lines + 1) + lon
                next_index = lat * (self.longitude_lines + 1) + lon + 1
                lines.append(Line(self.sphere_points[index], self.sphere_points[next_index]))

        # Longitude lines
        for lon in range(self.longitude_lines + 1):
            for lat in range(self.latitude_lines):
                index = lat * (self.longitude_lines + 1) + lon
                next_index = (lat + 1) * (self.longitude_lines + 1) + lon
                lines.append(Line(self.sphere_points[index], self.sphere_points[next_index]))

        return lines

    def create_shading_lines(self):
        lines = []
        for i in range(self.shading_density):
            theta1 = random.random() * math.pi
            phi1 = random.random() * 2 * math.pi

            # Bias toward front
            bias = random.random()
            use_bias = bias < 0.6
            final_phi1 = (phi1 * 0.5 + math.pi * 0.75) if use_bias else phi1

            theta2 = theta1 + (random.random() - 0.5) * 0.5
            phi2 = final_phi1 + (random.random() - 0.5) * 0.5

            x1 = self.radius * math.sin(theta1) * math.cos(final_phi1)
            y1 = self.radius * math.cos(theta1)
            z1 = self.radius * math.sin(theta1) * math.sin(final_phi1)

            x2 = self.radius * math.sin(theta2) * math.cos(phi2)
            y2 = self.radius * math.cos(theta2)
            z2 = self.radius * math.sin(theta2) * math.sin(phi2)

            lines.append(Line(Point3D(x1, y1, z1), Point3D(x2, y2, z2)))

        return lines

    def create_w_artifact(self):
        lines = []
        segments = 50
        w_width = math.pi / 12  # Half width
        w_height = 0.225  # Increased by 50%

        for i in range(segments):
            t = i / segments
            next_t = (i + 1) / segments

            # W shape function
            def w_shape(x):
                normalized = (x % 1) * 4
                if normalized < 1:
                    return normalized
                elif normalized < 2:
                    return 2 - normalized
                elif normalized < 3:
                    return normalized - 2
                else:
                    return 4 - normalized

            lat1 = (w_shape(t) - 0.5) * w_height
            lat2 = (w_shape(next_t) - 0.5) * w_height
            lon1 = t * w_width
            lon2 = next_t * w_width

            theta1 = math.pi / 2 - lat1
            phi1 = lon1
            theta2 = math.pi / 2 - lat2
            phi2 = lon2

            x1 = self.radius * math.sin(theta1) * math.cos(phi1)
            y1 = self.radius * math.cos(theta1)
            z1 = self.radius * math.sin(theta1) * math.sin(phi1)

            x2 = self.radius * math.sin(theta2) * math.cos(phi2)
            y2 = self.radius * math.cos(theta2)
            z2 = self.radius * math.sin(theta2) * math.sin(phi2)

            line = Line(Point3D(x1, y1, z1), Point3D(x2, y2, z2))
            line.is_artifact = True
            lines.append(line)

        return lines

    def rotate_x(self, point, angle):
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        return {
            'x': point.x,
            'y': point.y * cos_a - point.z * sin_a,
            'z': point.y * sin_a + point.z * cos_a
        }

    def rotate_y(self, point_or_dict, angle):
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)

        # Handle both Point3D objects and dictionaries
        if isinstance(point_or_dict, dict):
            x, y, z = point_or_dict['x'], point_or_dict['y'], point_or_dict['z']
        else:
            x, y, z = point_or_dict.x, point_or_dict.y, point_or_dict.z

        return {
            'x': x * cos_a + z * sin_a,
            'y': y,
            'z': -x * sin_a + z * cos_a
        }

    def project_3d(self, point):
        perspective = 800
        scale = perspective / (perspective + point.rotated_z)
        point.projected_2d_x = point.rotated_x * scale + self.center_x
        point.projected_2d_y = point.rotated_y * scale + self.center_y
        return scale

    def get_color_for_point(self, point):
        # Light source from front-top-left
        light_x = -0.5
        light_y = -0.7
        light_z = 1

        # Normalize point position
        normal_x = point.rotated_x / self.radius
        normal_y = point.rotated_y / self.radius
        normal_z = point.rotated_z / self.radius

        # Calculate lighting
        lighting = normal_x * light_x + normal_y * light_y + normal_z * light_z

        if lighting > 0.5:
            return random.choice(self.colors['light'])
        elif lighting > 0:
            return random.choice(self.colors['medium'])
        elif lighting > -0.3:
            return random.choice(self.colors['dark'])
        else:
            return random.choice(self.colors['shadow'])

    def hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def darken_color(self, hex_color, amount=20):
        r, g, b = self.hex_to_rgb(hex_color)
        r = max(0, r - amount)
        g = max(0, g - amount)
        b = max(0, b - amount)
        return f"#{r:02x}{g:02x}{b:02x}"

    def update_geometry(self, angle_y):
        # Update all points
        all_points = set()
        for line in self.all_lines:
            all_points.add(line.point1)
            all_points.add(line.point2)

        for point in all_points:
            # Apply axial tilt first, then rotation
            rotated = self.rotate_x(point, self.axial_tilt)
            rotated = self.rotate_y(rotated, angle_y)

            point.rotated_x = rotated['x']
            point.rotated_y = rotated['y']
            point.rotated_z = rotated['z']

            self.project_3d(point)

        # Update line colors
        for line in self.all_lines:
            mid_point = Point3D(
                (line.point1.rotated_x + line.point2.rotated_x) / 2,
                (line.point1.rotated_y + line.point2.rotated_y) / 2,
                (line.point1.rotated_z + line.point2.rotated_z) / 2
            )

            if line.is_artifact:
                # Make W orange when facing forward (positive Z)
                avg_z = (line.point1.rotated_z + line.point2.rotated_z) / 2
                if avg_z > 0:  # Facing forward
                    line.color = '#FF6B35'  # Bright orange
                else:
                    line.color = '#8B2E1F'  # Dark red for back side
                line.width = 8.0  # Much bolder lines
            else:
                line.color = self.get_color_for_point(mid_point)
                avg_z = (line.point1.rotated_z + line.point2.rotated_z) / 2
                line.width = 0.8 if avg_z > 0 else 0.4

    def draw_frame(self, angle_y):
        # Create image with transparent background
        img = Image.new('RGBA', (self.canvas_width, self.canvas_height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Update geometry
        self.update_geometry(angle_y)

        # Sort lines by depth
        sorted_lines = sorted(self.all_lines, key=lambda line:
                            (line.point1.rotated_z + line.point2.rotated_z) / 2)

        # Draw lines
        for line in sorted_lines:
            avg_z = (line.point1.rotated_z + line.point2.rotated_z) / 2
            opacity = int(255 * (0.9 if avg_z > 0 else 0.5))

            color = self.hex_to_rgb(line.color) + (opacity,)

            # Draw line with width simulation (multiple thin lines)
            width = max(1, int(line.width))
            for i in range(width):
                for j in range(width):
                    offset_x = i - width // 2
                    offset_y = j - width // 2
                    draw.line([
                        (line.point1.projected_2d_x + offset_x, line.point1.projected_2d_y + offset_y),
                        (line.point2.projected_2d_x + offset_x, line.point2.projected_2d_y + offset_y)
                    ], fill=color, width=1)

        return img

    def generate_gif(self, filename="mars-w-ornament.gif", frames=240, duration=33):
        print("Generating Mars W X-Mas Ornament GIF...")

        images = []
        start_angle = -math.pi / 6  # Start angle to show W earlier

        for frame in range(frames):
            angle_y = start_angle + (frame * 2 * math.pi) / frames
            img = self.draw_frame(angle_y)
            images.append(img)
            print(f"Generated frame {frame + 1}/{frames}")

        # Save as GIF
        print("Saving GIF...")
        images[0].save(
            filename,
            save_all=True,
            append_images=images[1:],
            duration=duration,
            loop=0,
            optimize=True
        )

        print(f"GIF saved as {filename}")

if __name__ == "__main__":
    generator = MarsGifGenerator()
    generator.generate_gif()