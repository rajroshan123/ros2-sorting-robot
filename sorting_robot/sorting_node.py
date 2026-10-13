import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class SortingNode(Node):

    def __init__(self):
        super().__init__('sorting_node')

        self.subscription = self.create_subscription(
            String,
            '/object_detected',
            self.object_callback,
            10
        )

        self.publisher = self.create_publisher(
            String,
            '/sorting_decision',
            10
        )

        self.get_logger().info('Sorting node started.')

    def object_callback(self, msg):
        color = msg.data.strip().upper()

        bins = {
            'RED': 'BIN_1',
            'GREEN': 'BIN_2',
            'BLUE': 'BIN_3'
        }

        decision = bins.get(color, 'UNKNOWN_OBJECT')

        output = String()
        output.data = decision
        self.publisher.publish(output)

        self.get_logger().info(
            f'Object: {color} -> Decision: {decision}'
        )


def main(args=None):
    rclpy.init(args=args)
    node = SortingNode()

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
