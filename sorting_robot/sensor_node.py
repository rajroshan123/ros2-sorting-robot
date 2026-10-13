import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class SensorNode(Node):

    def __init__(self):
        super().__init__('sensor_node')

        self.publisher = self.create_publisher(
            String,
            '/object_detected',
            10
        )

        self.colors = ['RED', 'GREEN', 'BLUE']
        self.index = 0

        self.timer = self.create_timer(
            2.0,
            self.publish_color
        )

        self.get_logger().info('Sensor node started.')

    def publish_color(self):
        msg = String()
        msg.data = self.colors[self.index]

        self.publisher.publish(msg)
        self.get_logger().info(
            f'Detected object: {msg.data}'
        )

        self.index = (self.index + 1) % len(self.colors)


def main(args=None):
    rclpy.init(args=args)
    node = SensorNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()